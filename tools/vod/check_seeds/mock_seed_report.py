#!/usr/bin/env python
# coding=utf-8
# author: Tang Hong
# 模拟SDK登录，并发送lsm report
# purpose: mock大量seed的汇报，使策略将其加入雷锋池
# 雷锋池可放入最大seed数：total_peers = 45 * (ppc/16)*rate
# 其中rate与时间有关：0-2:0.6,2-6:0.4,6-9:0.5,9-14:0.8,14-18:0.6,18-20:0.8,20-23:1,23-24:0.6
# 根据当前已有的seed数，计算还需mock的seed数，大于500个即可
# etcd地址：http://172.30.0.26:2379/v2/keys?recursive=true&sorted=true
# 查看雷锋池各file_id的seed数：http://172.30.0.41:9999/vodseeds/report/seed
# getseeds请求格式：172.30.0.18/getseeds?pid=00010023458C4980994A64F223C48C5C&fid=011AF9DA247941F9B2A8AE81DC72EB5E
# 需要的seeds数量以及种类在init_peer_ids_list.py中配置！！！

import inspect
import json
import time
import os
import sys
from libs.request.http_request import send_http_request
from libs.common.path import get_current_path

TS_HOST = "47.104.178.217"
TS_PORT = 80
POST = "POST"


def peer_login(pid, pub_ip, private_ip="192.168.2.25"):
    uri = "/session/peers/{0}".format(pid)
    body_data = {
        "version": "5.0.1",
        "natType": 3,
        "publicIP": pub_ip,
        "publicPort": 37334,
        "privateIP": private_ip,
        "privatePort": 37334,
        "stunIP": "118.190.148.163",
        "macs": {},
        "deviceInfo": {}
        }
    headers = {
        "Content-Type": "application/json"
    }
    send_http_request(
        POST,
        TS_HOST,
        TS_PORT,
        uri,
        headers,
        None,
        body_data
    )


def send_lsm_report(pid, fid, ppc, cppc, file_psize, fsize):
    uri = "/distribute/peers/{0}".format(pid)
    body_data = {
        "lsmTotal": 209715200,
        "lsmFree": 104857600,
        "diskTotal": 5766610944,
        "diskFree": 3662925824,
        "universe": True,
        "files": [{
            "file_id": fid,
            "ppc": ppc,
            "cppc": cppc,
            "psize": file_psize,
            "fsize": fsize,
            "percent": 100,
            "stat": "done"
        }]
    }
    headers = {
        "Content-Type": "application/json"
    }
    send_http_request(
        POST,
        TS_HOST,
        TS_PORT,
        uri,
        headers,
        None,
        body_data
    )


if __name__ == "__main__":
    # isp_province及IP映射关系表
    isp_pro_ip_list = {"100017_310000": "192.102.205.0",
                       "100026_410000": "42.225.2.2",
                       "000000_500000": "101.150.0.0"}

    # 发送lsm report对应的文件信息
    file_id = "011AF9DA247941F9B2A8AE81DC72EB5E"
    ppc = 304
    cppc = 1
    psize = 1392
    filesize = 1447161183

    # 将生成的peer_ids.txt的内容取出放入peer_ids_info
    with open("{0}/peer_ids.txt".format(get_current_path()), 'r') as f:
        peer_ids_info = json.loads(f.readline())

    # peer_ids_total用于存放所有的peer_ids，用于汇报lsm report
    peer_ids_total = []

    # 取isp_pro_ip_list中不同的isp_province对应的public后去登录对应的peers
    for isp_pro, ip in isp_pro_ip_list.items():
        public_ip = ip
        peer_ids = peer_ids_info.get(isp_pro)
        for peer_id in peer_ids:
            peer_login(peer_id, public_ip)
            print "SDK登录成功，对应的isp_province为：{0}".format(isp_pro)
            peer_ids_total.append(peer_id)
    print peer_ids_total

    # 循环汇报
    while True:
        for peer_id in peer_ids_total:
            send_lsm_report(peer_id, file_id, ppc, cppc, psize, filesize)
        print "SDK发送lsm report成功"
        # 每隔10min发送一次lsm全量报
        time.sleep(60*10)


