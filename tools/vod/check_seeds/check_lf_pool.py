#!/usr/bin/env python
# coding=utf-8
# Author=JKZ
# check seeds of lf pool ( Redis, key: {FOSC_<file_id>_<isp_id>} )
import inspect
import json
import os
import time
import logging
import sys
from rediscluster import StrictRedisCluster

startup_nodes = [{"host": "172.30.0.20", "port": 6379},
                 {"host": "172.30.0.21", "port": 6379},
                 {"host": "172.30.0.22", "port": 6379}]
rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

# get current dir path
file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
parent_path = os.path.dirname(file_path)

log_file = "{0}/stdout.log".format(parent_path)
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="")

ISP_LIST = ["100017", "100026", "000000"]  # use in FOSC
FID_URL = {
        "96A8329020C446B1A64F0527FB510399": "http://migu.x.00cdn.com/demo/4k/Detail_of_the_Earth.mkv",
    }


def get_file_ids():
    """
    redis cluster里面的{FOSC_<fileid>_<isp>}存储各个频道可用seed列表
    :return: 频道列表
    """
    match_keys = rc.keys("*FOSC*")
    file_ids = list()
    for i in match_keys:
        # print i
        split_key = i.split("_")[1:-1]
        fid = "_".join(split_key)
        file_ids.append(fid)

    return list(set(file_ids))


def get_file_all_seeds(file_id):
    """
    通过file_id获得该频道可用seed列表
    :param file_id:
    :return:
    """
    file_seeds = list()
    isp_seeds_count = dict()
    for isp in ISP_LIST:
        fosc_key = "{FOSC_" + str(file_id) + "_" + str(isp) + "}"
        isp_seeds = rc.smembers(fosc_key)
        isp_seeds_count[isp] = len(isp_seeds)
        # print isp, "seeds count:", len(isp_seeds)
        for seed in isp_seeds:
            file_seeds.append(json.loads(seed))

    file_seeds_log = "File_id:"+str(file_id).ljust(32, ' ')+"; seeds count: "+str(len(file_seeds)).ljust(5, ' ')+\
                     str(isp_seeds_count).ljust(45, ' ')
    logging.debug(file_seeds_log)

    return file_seeds


def check_seeds(file_seeds, file_id=""):
    """
    遍历seeds列表，检查是否有出现次数大于1的seed
    :param file_seeds: seeds列表
    :return:
    """
    ids = dict()
    for i in file_seeds:
        peer_id = i.get("peer_id")
        ids[peer_id] = ids.setdefault(peer_id, 0) + 1
    if len(file_seeds) != len(ids):
        logging.error("".ljust(60, '*') + " Duplicated ! FILE_ID: "+str(file_id))
        for key, value in ids.items():
            if value > 1:
                # print key
                logging.error("".ljust(60, '*') + " Peer_id: "+str(key)+"; count: "+str(value))
        return False
    else:
        return True


if __name__ == "__main__":
    while True:
        file_id_list = get_file_ids()
        if len(file_id_list) > 0:
            logging.debug("{0} {1} {0}".format("".ljust(80, '-'), time.ctime()))
            for file_id in file_id_list:
                file_seeds = get_file_all_seeds(file_id=file_id)
                check_seeds(file_seeds=file_seeds, file_id=file_id)
        time.sleep(60)



