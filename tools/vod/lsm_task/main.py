#!/usr/bin/env python
#  coding=utf-8
# author: Tang Hong
# 模拟courier重复对SDK下发文件下载及删除任务
# purpose: 验证SDK的空洞能够被回收且meta文件最大值不超过文件个数乘以MAX(单个文件占用bet)]
import os
import subprocess
import paramiko
import inspect
import json
import sys
import requests
import time
import math
from libs.common.parse_response import *
import random

cppc = 1
# push_ip = "192.168.1.214"
push_ip = "118.190.153.230"
peer_id = "00010023458C4980994A64F223C48C5C"
# stun_hub_ip = "192.168.1.245"
stun_hub_ip = "172.30.0.25"
sdk_ip = "192.168.2.35"
distribute_task_url = "http://{0}:8000/distribute_task".format(stun_hub_ip)
ajax_distribute_url = "http://{0}:32717/ajax/distribute".format(sdk_ip)
ajax_lsm_url = "http://{0}:32717/ajax/lsm".format(sdk_ip)
REMOTE_FILE_PATH = "/home/admin/yunshang/yunshang.meta"
LOCAL_FILE_PATH = "D:/test/yunshang.meta"
SSH_PORT = 22
user = "root"
password = "root"
local_file_path = "D:/test/ys_service_static"
remote_file_path = "/home/admin/ys_service_static"


# 将ys_service_static文件拷贝至远程linux机器
def init_sdk():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(sdk_ip, SSH_PORT, user, password)
    cmd1 = "killall ys_service_static ;cd /home/admin; rm * -rf"
    ssh.exec_command(cmd1)
    sftp = ssh.open_sftp()
    sftp.put(local_file_path, remote_file_path)
    print "ys_service_static拷贝至Linux成功"
    sftp.close()
    cmd2 = "cd /home/admin; chmod +x ys_service_static; ./ys_service_static"
    ssh.exec_command(cmd2)
    print "SDK启动成功"
    ssh.close()


# distribute download_tasks
def download_files(file_list):
    """
    下载指定列表的文件
    :param file_list: 里面都是file_id
    :return:
    """
    body = []
    for file1 in file_list:
        for file2 in all_files:
            if file1 == file2.get("file_id"):
                download_file_id = file2.get("file_id")
                ppc = file2.get("ppc")
                file_size = file2.get("file_size")
                piece_size = file2.get("piece_size")
                # print file_id, ppc, file_size, piece_size
                body.append(
                    dict(file_id=download_file_id, operation="download", file_size=file_size, piece_size=piece_size,
                         ppc=ppc, cppc=cppc, priority=1, push_port=80, push_ip=push_ip, peer_id=peer_id)
                )
    requests.post(distribute_task_url, json=body)
    # print body


def delete_file(file_list):
    body = []
    for delete_file_id in file_list:
        body.append(
            {
                "file_id": delete_file_id,
                "operation": "delete",
                "peer_id": peer_id
            }
        )
    requests.post(distribute_task_url, json=body)
    # print body


# check ajax/distribute page
def check_ajax_distribute():
    ajax_distribute_data = requests.get(ajax_distribute_url)
    # files not downloading in cache
    cache_task = list()
    # 获取当前SDK缓存队列中的文件列表
    cache_file_count = get_response_data_by_path(ajax_distribute_data, "/task_count")
    if cache_file_count is 0:
        print "SDK has 0 file in cache"
    else:
        count = 0
        while count < cache_file_count:
            num = str(count)
            path = "/task_list/" + num
            # print path
            task_list = get_response_data_by_path(ajax_distribute_data, path)
            file_name = task_list.get("file_id")
            count = count + 1
            cache_task.append(file_name)
        print "The following {0} files are in cache task list".format(cache_file_count)
        print cache_task
    return cache_task


# 获取ajax/lsm页面上SDK已缓存和正在缓存的文件信息
def get_lsm_files():
    having_files = list()
    ajax_lsm_data = requests.get(ajax_lsm_url)
    het_data = get_response_data_by_path(ajax_lsm_data, "/meta/het")
    for key, downloaded_file_id in het_data.items():
        if key != "head" and key != "dirty":
            having_files.append(downloaded_file_id)
    return having_files


# 统计SDK的yunshang.data,yunshang.meta,lsmfree的值
def calc_lsm_value():
    wait_task = check_ajax_distribute()
    having_files = get_lsm_files()
    all_lsm_files = having_files
    for wait_file in wait_task:
        if wait_file not in having_files:
            all_lsm_files.append(wait_file)
    bet_value = 0
    data_value = 0
    for filename in all_lsm_files:
        for filename2 in all_files:
            if filename == filename2.get("file_id"):
                file_size = filename2.get("file_size")
                ppc = filename2.get("ppc")
                piece_size = filename2.get("piece_size")
                chunk_gross = math.ceil((float(file_size) / int(ppc) / int(piece_size)))
                # 计算单个文件占用的chunk_gross值
                single_file_data = chunk_gross * (int(piece_size) + 32)
                data_value = single_file_data + data_value
                # 单个文件占用bet空间计算公式：chunk_gross*5 + 298 byte
                bet_value = chunk_gross * 5 + bet_value + 298
                # bet_value_list.append(bet_value)
    # meta_value:SDK总的meta值计算公式：1118368（meta初始值）+864（bet初始值）+bet_value（单个文件占用的bet值）
    meta_value = 1118368 + 864 + bet_value
    print "yunshang.meta's filesize should be {0} byte".format(meta_value)
    print "yunshang.data's filesize should be {0} byte".format(data_value)
    print "SDK lsmfree should be {0} byte".format(209715200 - data_value)


# 计算重复下载删除后meta文件的最大值
def calc_max_lsm_value():
    bet_value = 0
    bet_value_list = list()
    for filename in all_files:
        file_size = filename.get("file_size")
        ppc = filename.get("ppc")
        piece_size = filename.get("piece_size")
        chunk_gross = math.ceil((float(file_size) / int(ppc) / int(piece_size)))
        # 单个文件占用bet空间计算公式：chunk_gross*5 + 298 byte
        bet_value = chunk_gross * 5 + bet_value + 298
        bet_value_list.append(bet_value)
    max_meta_value = len(file_ids) * max(bet_value_list) + 1118368 + 864
    print "SDK重复下载删除的文件个数为{0},占用bet空间最大的值为:{1}byte..." \
          "因此SDK的meta文件大小不应超过{0}*{1}+1118368+864={2}byte"\
        .format(len(file_ids), max(bet_value_list), max_meta_value)
    # 如果实在linux运行的，执行get_meta_fsize()
    # meta_size = get_meta_fsize()
    # 如果是在Android运行的，执行adb_get_meta_fsize()
    meta_size = adb_get_meta_fsize()
    if int(meta_size) < int(max_meta_value):
        print "当前yunshang.meta的值为{0}byte，未超过max_meta_value:{1},meta回收功能OK".format(meta_size, max_meta_value)
    else:
        print "当前yunshang.mata的值为{0}byte，超过max_meta_value:{1},meta回收功能失败".format(meta_size, max_meta_value)


def get_meta_fsize():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(sdk_ip, SSH_PORT, user, password)
    cmd = "du -sb /home/admin/yunshang/yunshang.meta | awk '{print $1}'"
    # print "{0} run command :".format(sdk_ip), cmd
    stdin, stdout, stderr = ssh.exec_command(cmd)
    meta_size = stdout.read().strip()
    # print meta_size
    ssh.close()
    return meta_size


def adb_get_meta_fsize():
    command = "adb shell ls -l /sdcard/yunshang/yunshang.meta"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    file_line = process.stdout.readlines()[0]
    outline_list = file_line.split()
    meta_size = outline_list[3]
    # print meta_size
    return meta_size


if __name__ == "__main__":
    # 将ys_service_static拷贝至远程机器上
    # init_sdk()
    # time.sleep(30)
    # 获得文件列表
    file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
    parent_path = os.path.dirname(file_path)
    f = open("{0}/all_files.txt".format(parent_path), 'r')
    all_files = json.loads(f.readline())
    f.close()
    file_ids = list()
    for fil in all_files:
        file_id = fil.values()[2]
        file_ids.append(file_id)
    print "MySQL has these files:{0}".format(file_ids)

    # 先初始化含6个文件的列表，让SDK去缓存
    init_file_list = file_ids[0:5]
    # print init_file_list
    download_files(init_file_list)
    downloaded_files = list()
    # 当lsm页面已缓存文件数为6时，删除3个文件
    distribute_count = 0
    while True:
        if len(get_lsm_files()) < 5:
            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print "now time is {0},SDK is downloading files, please wait few minutes".format(now_time)
            # 每隔1min查询一次已缓存的文件数
            time.sleep(60)
        else:
            print "5 files are done... "
            print "当前SDK的ajax/lsm页面已缓存或正在缓存的文件:{0}".format(get_lsm_files())
            calc_max_lsm_value()
            print "next,we will delete 1 files"
            # 此时缓存文件数已达6，将已缓存的文件信息取出
            downloaded_files = get_lsm_files()
            # 打乱文件顺序后，取前1个文件
            random.shuffle(downloaded_files)
            delete_file_list = list()
            delete_file_list.append(downloaded_files[0])
            # 下发1个文件删除任务
            delete_file(delete_file_list)
            time.sleep(30)
            print "delete success"
            for file in delete_file_list:
                for file2 in all_files:
                    if file == file2.get("file_id"):
                        file_size = file2.get("file_size")
                        ppc = file2.get("ppc")
                        piece_size = file2.get("piece_size")
                        print "当前删除的文件是:{0},filesize={1},ppc={2},piece_size={3}"\
                            .format(delete_file_list, file_size, ppc, piece_size)
            # 将未下发过的文件信息取出
            not_downloaded_files = [file for file in file_ids if file not in downloaded_files]
            # 打乱文件顺序后，取前1个文件
            random.shuffle(not_downloaded_files)
            # print not_downloaded_files
            ready_files_list = list()
            ready_files_list.append(not_downloaded_files[0])
            for file in ready_files_list:
                for file2 in all_files:
                    if file == file2.get("file_id"):
                        file_size = file2.get("file_size")
                        ppc = file2.get("ppc")
                        piece_size = file2.get("piece_size")
                        print "当前下载的文件是:{0},filesize={1},ppc={2},piece_size={3}"\
                            .format(ready_files_list, file_size, ppc, piece_size)
            # 下发1个文件下载任务
            download_files(ready_files_list)
            distribute_count = distribute_count + 1
            print "第{0}次删除、下载执行完成".format(distribute_count)
