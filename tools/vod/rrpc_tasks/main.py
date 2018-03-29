#!/usr/bin/env python
# coding=utf-8
# Author=JKZ
# distribute download tasks and delete tasks to seed repeatedly
import inspect
import os
import random
import json
import requests
import time
import sys
from rediscluster import StrictRedisCluster
import logging

REQUEST_HEADERS_JSON = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Connection": "close",
    # "User-Agent": "YunshangSDK/4.2.7"
}
STUN_HUB_HOST = "172.30.0.25:8000"
VOD_PUSH_PUBLIC_IP = "118.190.153.230"

# redis集群
redis_startup_nodes = [{"host": "172.30.0.20", "port": 6379},
                       {"host": "172.30.0.21", "port": 6379},
                       {"host": "172.30.0.22", "port": 6379}]
# get current dir path
file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
parent_path = os.path.dirname(file_path)

# 配置log文件
log_file = "{0}/stdout.log".format(parent_path)
logging.basicConfig(filename=log_file, level=logging.ERROR, format="[%(asctime)s]-%(levelname)s: %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(name)-12s %(levelname)-8s] %(message)s')
console.setFormatter(formatter)
logger = logging.getLogger('rrpc_tasks')
logger.setLevel(level=logging.INFO)
logger.addHandler(console)


def get_online_pids_from_redis(peer_prefix="00010048"):
    """
    获得redis cluster里面所有的已登录节点peer id
    :param peer_prefix: prefix视情况修改
    :return:
    """
    rc = StrictRedisCluster(startup_nodes=redis_startup_nodes, decode_responses=True)
    match_keys = rc.keys("PNIC_{0}*".format(peer_prefix))
    peer_id_list = list()
    for i in match_keys:
        peer_id = i.replace("PNIC_", "")
        peer_id_list.append(str(peer_id))
    return peer_id_list


def create_distribute_task(peer_id, operation, file_id, file_size=None, piece_size=None, ppc=None):
    """
    生成下载/删除任务
    :param peer_id: 节点唯一标识
    :param operation: "download" or "delete"
    :param file_id:
    :param file_size:
    :param piece_size:
    :param ppc:
    :return:
    """
    task = {
        "file_id": str(file_id),
        "peer_id": str(peer_id),
        "operation": operation
    }
    if operation == "download":
        download_info = {
            "file_size": int(file_size),
            "piece_size": int(piece_size),
            "ppc": int(ppc),
            "cppc": 1,
            "priority": 0,
            "push_port": 80,
            "push_ip": VOD_PUSH_PUBLIC_IP

        }
        task.update(download_info)
    return task


def send_distribute_tasks_to_stun_hub(stun_hub_host, req_data):
    """
    向stun-hub发送节点下载/删除任务
    :param stun_hub_host:
    :param req_data: [task1,task2]
    :return:
    """
    try:
        response = requests.post("http://{0}/distribute_task".format(stun_hub_host), headers=REQUEST_HEADERS_JSON,
                                 data=json.dumps(req_data))
        succ_task_count = response.json().get("succ_task_count")
        if succ_task_count != len(req_data):
            # logger.error("Expect succ task count: {0}, actual count: {1}".format(len(req_data), succ_task_count))
            pids = []
            for task in req_data:
                pid = task.get("peer_id")
                pids.append(pid)
            logger.error(
                "Distribute tasks fail. Peer_ids: {0}, stun-hub response: {1} {2}".format(pids, response.status_code,
                                                                                          response.content))
            # logger.error("Request body: {0}".format(req_data))
    except Exception, error:
        logger.critical("Exception：{0}".format(error))


def distribute_tasks_repeatedly(peer_ids, download_files, delete_files, loop_times=50):
    """
    针对指定节点反复下发下载、删除任务
    :param peer_ids: 指定的一个节点或批量节点
    :param download_files: 节点要执行下载任务的文件信息
    :param delete_files: 节点要执行删除任务的文件信息
    :param loop_times: 反复下发任务的执行次数
    :return:
    """
    if type(peer_ids) != list:
        peer_ids = [peer_ids]
    if type(download_files) != list:
        download_files = [download_files]
    if type(delete_files) != list:
        delete_files = [delete_files]
    for i in range(loop_times):
        # 下发删除任务
        logger.info("Prepare distribute delete tasks.")
        for pid in peer_ids:
            req_data = []
            for delete_file in delete_files:
                file_id = delete_file.get("file_id")
                task = create_distribute_task(pid, operation="delete", file_id=file_id)
                req_data.append(task)
            send_distribute_tasks_to_stun_hub(STUN_HUB_HOST, req_data)
        time.sleep(10)

        # 下发下载任务
        logger.info("Prepare distribute download tasks.")
        for pid in peer_ids:
            req_data = []
            for download_file in download_files:
                file_id = download_file.get("file_id")
                file_size = download_file.get("file_size")
                piece_size = download_file.get("piece_size")
                ppc = download_file.get("ppc")
                task = create_distribute_task(pid, "download", file_id, file_size, piece_size, ppc)
                req_data.append(task)
            send_distribute_tasks_to_stun_hub(STUN_HUB_HOST, req_data)
        # 等待下载完成
        time.sleep(900)


if __name__ == "__main__":
    # 确定file id
    files_source = "mysql"
    if files_source == "mysql":
        # run get_files.py to update all_files.txt
        os.system("python get_files.py")
        time.sleep(3)
        f = open("{0}/all_files.txt".format(parent_path), 'r')
        all_files = json.loads(f.readline())
        f.close()
    else:
        # 指定文件下发任务
        file_keys = ["file_id", "file_size", "piece_size", "ppc"]
        files_list = [
            ("58978B0E0EB84A7AB93A0487D628C44F", 172917700, 1392, 32),
            ("80E855957F404713A32222DF6531F64C", 172917700, 1392, 32),
        ]
        all_files = list()
        for f in files_list:
            file_info = dict(zip(file_keys, f))
            all_files.append(file_info)

    random.shuffle(all_files)
    # 最多下发3个文件下载任务，下发删除任务时删除所有文件
    download_task_files = all_files[:min(len(all_files), 3)]
    delete_task_files = all_files

    f = open("{0}/peer_id.txt".format(parent_path), 'r')
    file_peer_ids = json.loads(f.readline())
    f.close()

    logger.info("Action")
    logger.info("Download files: \n{0}".format(str(download_task_files).replace("},", "}\n")))
    logger.info("Delete files: \n{0}".format(str(delete_task_files).replace("},", "}\n")))
    while True:
        # peer_ids = get_online_pids_from_redis(peer_prefix="00010048")
        pids = file_peer_ids
        logger.info("Load peer_id num: {0}".format(len(pids)))
        distribute_tasks_repeatedly(pids, download_task_files, delete_task_files)
