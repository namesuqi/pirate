#!/usr/bin/env python
# coding=utf-8
# author: mao yu nan

# 测试内存置换策略的主程序

import threading
from multiprocessing import Process
import time
from config_loader import Loader
from downloader import sdk_download
from log import Log

loader = Loader()
config_info = loader.load_config_file()
sdks_get_file_dict = config_info['sdks_get_file_dict']
file_info = config_info['files_info']
start_chunk_id = config_info['start_chunk_id']
continue_requeste_interval = config_info['sdk_continue_requeste_interval']
threads = []
random_cri = []

# 总数接近600个SDK节点
total_sdk_num = 600
process_num = 16   # 和机器CPU数量保持一致
thread_num = int(total_sdk_num/process_num)
file_size = 5000   # 单位M Bytes
ppc = 304


def start_fake_sdks(thread_nums, process_name, file_id, fsize):
    t_pool = list()
    log = Log('log', 'sdk_faker.log')
    for num in range(thread_nums):
        thread = threading.Thread(target=sdk_download, args=(
            process_name,
            num,
            fsize,
            file_id,
            ppc,
            log,
            start_chunk_id
        ))
        thread.setDaemon(True)
        t_pool.append(thread)

    for t in t_pool:
        t.start()
        time.sleep(1)

    for t in t_pool:
        t.join()


def main_function_1():
    t_pool = list()
    log = Log('log', 'sdk_faker.log')
    for num in range(20):
        thread = threading.Thread(target=sdk_download, args=(
            8,
            num,
            10000,
            '561B90A24D754AC6FAFF7D3A54E9DA2D',
            ppc,
            log,
            start_chunk_id
        ))
        thread.setDaemon(True)
        t_pool.append(thread)
    for num in range(20, 22):
        thread = threading.Thread(target=sdk_download, args=(
            8,
            num,
            10000,
            '561B90A24D754AC6FAFF7D3A54E9DA2E',
            ppc,
            log,
            start_chunk_id
        ))
        thread.setDaemon(True)
        t_pool.append(thread)

    for t in t_pool:
        t.start()

    for t in t_pool:
        t.join()


if __name__ == '__main__':
    start_time = time.time()

    process_list = list()
    file_ids = [
        "561B90A24D754AC6FAFF7D3A54E9DA2A",
        "561B90A24D754AC6FAFF7D3A54E9DA2B",
        "561B90A24D754AC6FAFF7D3A54E9DA2C",
        "561B90A24D754AC6FAFF7D3A54E9DA2D",
        "561B90A24D754AC6FAFF7D3A54E9DA2E"
        ]
    for i in range(process_num):
        if i < 8:
            p = Process(target=start_fake_sdks, args=(thread_num, i, file_ids[0], file_size))
        elif i < 13:
            p = Process(target=start_fake_sdks, args=(thread_num, i, file_ids[1], file_size))
        elif i < 16:
            p = Process(target=start_fake_sdks, args=(thread_num, i, file_ids[2], file_size))
        else:
            break
        process_list.append(p)
        # elif i < 8:
        #     p = Process(
        #         target=main_function_1, args=())
        #     p.daemon = True
        #     p.start()
        #     process_list.append(p)

    # start
    for p in process_list:
        p.daemon = True
        p.start()

    # wait for end
    for p in process_list:
        p.join()

    print 'finish all cost:{0}s'.format(time.time() - start_time)
