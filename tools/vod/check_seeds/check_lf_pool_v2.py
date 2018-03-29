# coding=utf-8
# Author=JKZ
# check seeds of lf pool ( Redis, key: {FOSC_<file_id>}_<isp_group>_<provice_group> )
import json
import time
import logging
from rediscluster import StrictRedisCluster

startup_nodes = [{"host": "172.30.0.20", "port": 6379},
                 {"host": "172.30.0.21", "port": 6379},
                 {"host": "172.30.0.22", "port": 6379}]
rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
log_file = "/home/admin/pt_zsw/stdout.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="")


def get_file_ids():
    """
    通过匹配FOSC获取所有有雷锋节点的file_id
    :return:
    """
    match_keys = rc.keys("*FOSC*")
    file_ids = list()
    for i in match_keys:
        # print i
        fid = i.split("}")[0].replace("{FOSC_", "")
        file_ids.append(fid)

    return list(set(file_ids))


def get_file_all_seeds(file_id):
    """
    通过file_id获取其对应的所有fosc key并按group（isp, provice）进行统计
    :param file_id:
    :return:
    """
    file_seeds = list()
    file_group_seeds_count = dict()
    file_seeds_keys = rc.keys("{FOSC_%s}*" % file_id)
    for fosc_key in file_seeds_keys:
        # isp_group, provice_group = fosc_key.split("_")[-2:]
        group = fosc_key.split("}_")[-1]  # IspGroup_ProvinceGroup
        file_group_seeds = rc.smembers(fosc_key)
        file_group_seeds_count[group] = len(file_group_seeds)

        for seed in file_group_seeds:
            file_seeds.append(json.loads(seed))

    file_seeds_log = "File_id:"+str(file_id).ljust(32, ' ')+"; seeds count: "+str(len(file_seeds)).ljust(5, ' ')+\
                     str(file_group_seeds_count).ljust(45, ' ')+"; "
    logging.debug(file_seeds_log)

    return file_seeds


def check_seeds(file_seeds, file_id=""):
    """
    检查seeds中是否有重复peer_id
    :param file_seeds:
    :param file_id:
    :return:
    """
    ids = dict()
    for i in file_seeds:
        peer_id = i.get("peer_id")
        ids[peer_id] = ids.setdefault(peer_id, 0) + 1
    if len(file_seeds) != len(ids):
        logging.debug("".ljust(60, '*') + " Duplicated ! FILE_ID: "+str(file_id))
        for key, value in ids.items():
            if value > 1:
                # print key
                logging.debug("".ljust(60, '*') + " Peer_id: "+str(key)+"; count: "+str(value))
        return False
    else:
        return True


if __name__ == "__main__":

    while True:
        logging.debug("{0} {1} {0}".format("".ljust(80, '-'), time.ctime()))
        file_id_list = get_file_ids()
        for file_id in file_id_list:
            file_seeds = get_file_all_seeds(file_id=file_id)
            check_seeds(file_seeds=file_seeds, file_id=file_id)
        time.sleep(60)
        logging.debug("")

