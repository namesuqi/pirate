#!/usr/bin/env python
# coding=utf-8
# author=zengyuetian
# get peer id according to host.ini
# copy peer id txt file to rrpc_tasks dir
# 用于反复下发下载删除任务

import json
import requests
import threading
import time
import os
import inspect
import sys
import ConfigParser

SDK_PORT_START = 30000
SDK_PORT_STEP = 10


# get current dir path
file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
parent_path = os.path.dirname(file_path)
vod_tool_path = os.path.dirname(parent_path)
rrpc_tool_path = vod_tool_path + "/rrpc_tasks"
INI_FILE = 'host.ini'
mutex = threading.Lock()
peer_ids = list()


def get_id_by_ajax(ip, num, port):
    distance = 0
    for i in range(num):
        t = threading.Thread(target=get_peer_id, args=(ip, port + distance))
        t.start()
        time.sleep(0.01)
        distance += SDK_PORT_STEP

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()


def get_peer_id(ip, port):
    print(ip, port)
    url = "http://{0}:{1}{2}".format(ip, port, "/ajax/conf")
    headers = dict()
    headers["accept"] = 'application/json'
    headers["content-type"] = 'application/json'
    res = requests.get(url, headers=headers, timeout=5)
    peer_id = json.loads(res.content).get("peer_id", None)
    if mutex.acquire(1):
        peer_ids.append(peer_id)
        mutex.release()


def read_ini():
    """
    get configure info from ini file
    :return: None
    """
    config = ConfigParser.ConfigParser()
    config.readfp(open(INI_FILE_PATH))
    section_list = config.sections()
    for i in section_list[1:]:
        if config.has_section(i):
            SDK_IP_LIST.append(config.get(i, "IP"))
            SDK_NUM_LIST.append(int(config.get(i, "SDK_Number")))
        else:
            break

if __name__ == "__main__":
    peer_id_txt = 'peer_id.txt'
    SDK_IP_LIST = []
    SDK_NUM_LIST = []

    INI_FILE_PATH = "{0}/{1}".format(parent_path, INI_FILE)

    read_ini()
    print SDK_IP_LIST
    start_time = time.time()

    for index, ip in enumerate(SDK_IP_LIST):
        num = SDK_NUM_LIST[index]
        get_id_by_ajax(ip, num, SDK_PORT_START)

    print peer_ids
    end_time = time.time()

    fp = file(peer_id_txt, 'w')
    json.dump(peer_ids, fp)
    fp.close()

    print("Get peer id num: {0}".format(len(peer_ids)))
    print("Please check id.txt for peer ids.")
    print("Done, cost {0} seconds.".format(end_time-start_time))

    # copy peer_id.txt to rrpc_task tool folder
    print(parent_path, rrpc_tool_path)
    copy_cmd = "cp {0}/{1} {2}".format(parent_path, peer_id_txt, rrpc_tool_path)
    os.system(copy_cmd)


