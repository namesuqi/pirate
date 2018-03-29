# main function query memory conversion strategy effect

import threading
import time
from multiprocessing import Process
from config_loader import Loader
from faker import fake_sdk
from log import Log

loader = Loader()
config_info = loader.load_config_file()
sdks_get_file_dict = config_info['sdks_get_file_dict']
file_info = config_info['files_info']
start_chunk_id = config_info['start_chunk_id']
continue_requeste_interval = config_info['sdk_continue_requeste_interval']
threads = []
random_cri = []


def main_function(thread_nums, process_name, file_id, file_size):
    t_pool = list()
    log = Log('log', 'sdk_faker.log')
    ppc = 304
    for num in range(thread_nums):
        thread = threading.Thread(target=fake_sdk, args=(
            process_name,
            num,
            file_size,
            file_id,
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
    process_num = 8
    thread_num = 37
    process_list = list()
    file_ids = [
        "561B90A24D754AC6FAFF7D3A54E9DA2A",
        "561B90A24D754AC6FAFF7D3A54E9DA2B",
        "561B90A24D754AC6FAFF7D3A54E9DA2C",
        "561B90A24D754AC6FAFF7D3A54E9DA2D",
        "561B90A24D754AC6FAFF7D3A54E9DA2E"
        ]
    for i in range(process_num):
            p = Process(
                target=main_function, args=(
                    thread_num, i, file_ids[0], 5000))
            p.daemon = True
            p.start()
            process_list.append(p)

    for p in process_list:
        p.join()
    print 'finish all cost:{0}s'.format(time.time())