#!/usr/bin/env python
# coding=utf-8
# Author=JKZ
# check seeds from ts
# 登录不同运营商的节点
# 获得可用的频道列表和用户
# 通过起播频道start channel获得file_id
# 通过get seeds 获得seeds列表
# 去重，检查seeds列表是否有重复
# 记录日志


import inspect
import json
import logging
import os
import requests
import time
import sys

# from misc.tools.lf_pool.check_ip import checkTaobaoIP

# get current dir path
file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
parent_path = os.path.dirname(file_path)

# 配置日志
log_file = "{0}/stdout.log".format(parent_path)
logging.basicConfig(filename=log_file, level=logging.ERROR, format="[%(asctime)s]-%(levelname)s: %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logger = logging.getLogger('check_seeds')
logger.setLevel(level=logging.INFO)
logger.addHandler(console)

# 服务器IP地址和端口
# TS_HOST = "118.31.134.23:80"  # ONLINE_PRD
TS_HOST = "47.104.178.217:80"  # ONLINE_TEST
CHANNEL_HOST = "47.104.178.217:80"  # ONLINE_TEST

# 通用header
request_headers_json = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Connection": "close",
    # "User-Agent": "YunshangSDK/4.2.7"
}
# 加Host字段
headers_ts = request_headers_json.copy()
headers_ts.update({"Host": "ts.crazycdn.com"})
headers_seeds = request_headers_json.copy()
headers_seeds.update({"Host": "seeds.crazycdn.com"})
headers_channel = request_headers_json.copy()
headers_channel.update({"Host": "live-ch.crazycdn.com"})


def get_file_url_user_by_playlist():
    """
    解析播放列表，获得{file_url: [username, file_type]}的字典并返回
    :return:
    """
    response = requests.get("http://videolist.cloutropy.com/playlist/playlist_4k")
    result = {}
    files = response.content.split("\n")
    for f in files:
        f = f.split(";")
        if len(f) == 5:
            file_type = f[0]  # "vod", "hls"
            file_url = f[2]
            username = f[4]
            result[file_url] = [username, file_type]
    return result


def get_file_id(file_url, username="demo", file_type="vod"):
    """
    通过start channel向channel获取file id
    :param file_url:
    :param username:
    :param file_type: 播放文件类型
    :return:
    """
    if file_type == "vod":
        request_url = "http://{0}/startchannel?user={1}&pid={2}&url={3}".format(CHANNEL_HOST, username, "".zfill(32),
                                                                                file_url)
        response = requests.get(request_url, headers=headers_channel)
        file_id = response.json().get("file_id")
    elif file_type == "hls":
        request_url = "http://{0}/starthls?user={1}&pid={2}&url={3}".format(CHANNEL_HOST, username, "".zfill(32),
                                                                            file_url)
        response = requests.get(request_url, headers=headers_channel)
        file_id = response.json().get("data_file_id")
    else:
        print "start channel fail, file_url: %s" % file_url
        file_id = None
    return file_id


def get_seeds(peer_id, file_id):
    """
    通过getseeds向TS获取seeds列表
    :param peer_id:
    :param file_id:
    :return:
    """
    request_url = "http://{0}/getseeds?pid={1}&fid={2}".format(TS_HOST, peer_id, file_id)
    response = requests.get(request_url, headers=headers_seeds)
    try:
        seeds_list = response.json().get("seeds")
        logger.debug("http://seeds.crazycdn.com/getseeds?pid={0}&fid={1}".format(peer_id, file_id))
        logger.debug(seeds_list)
    except:
        print "get seeds fail"
        seeds_list = None
    return seeds_list


def check_seeds(file_seeds):
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
        logging.error("".ljust(60, '*') + str(time.ctime()) + " Duplicated !")
        for key, value in ids.items():
            if value > 1:
                logging.error("".ljust(60, '*') + " seed peer_id: " + str(key) + "; count: " + str(value))
        return False
    else:
        return True


if __name__ == "__main__":
    # 获取file_ids
    file_url_user_dict = get_file_url_user_by_playlist()
    fid_list = []
    for k, v in file_url_user_dict.iteritems():
        username, file_type = v
        fid = get_file_id(file_url=k, username=username, file_type=file_type)
        if fid is not None:
            fid_list.append(fid)

    # 准备多个区域的节点用于getseeds
    login_body = {
        "version": "5.0.1",
        "natType": 0,
        "publicIP": "116.231.59.90",
        "publicPort": 12345,
        "privateIP": "192.168.2.22",
        "privatePort": 12345,
        "stunIP": "118.31.2.166",
        "macs": {}
    }
    PIDS = [
        "0001002378274C7BB0DECAFBF1575000",
        "0001002378274C7BB0DECAFBF1575001",
        "0001002378274C7BB0DECAFBF1575002"
    ]
    # GROUP: ISP_PROVINCE
    GROUP_IPS = {
        "100017_310000": "116.231.59.90",
        "100026_310000": "27.115.0.0",
        "000000_310000": "211.136.173.172"
    }
    j = 0
    group_pids = {}
    for group, ip in GROUP_IPS.iteritems():
        pid = PIDS[j]
        login_body["publicIP"] = ip
        # send login request
        requests.post("http://{0}/session/peers/{1}".format(TS_HOST, pid), data=json.dumps(login_body),
                      headers=headers_ts)
        group_pids[str(group)] = pid
        j += 1
    logger.info("{0}".format(group_pids))

    while True:
        for pid in group_pids.values():
            # send heartbeat request
            requests.get("http://{0}/session/peers/{1}".format(TS_HOST, pid), headers=headers_ts)

        for fid in fid_list:
            for isp, pid in group_pids.iteritems():
                seeds = get_seeds(peer_id=pid, file_id=fid)
                try:
                    seeds_count = len(seeds)
                except:
                    seeds_count = 0
                logger.info("Fid: {0}, player isp: {1}, get seeds count: {2}".format(fid, isp, seeds_count))
                if seeds_count != 0:
                    if not check_seeds(seeds):
                        logger.error("Seeds duplicated !!!")
                        logger.error("Fid: {0}, peer isp_province: {1}, paler peer_id: {2}, seeds count: {3}.".format(
                            fid, isp, pid, seeds_count))

                        # get isp and province by seed publicIP
                        # s = sorted(seeds, key=lambda seed: seed["publicIP"])
                        # ips = dict()
                        # for i in s:
                        #     pub_ip = i.get("publicIP")
                        #     ips[pub_ip] = ips.setdefault(pub_ip, 0) + 1
                        # for key, value in ips.items():
                        #     if value > 1:
                        #         iploc = checkTaobaoIP(key)
                        #         print value, iploc

        time.sleep(60)
