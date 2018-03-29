# coding=utf-8
# simulate sdk behavior
# author: myn
import time
import math
import urllib2
from config_loader import Loader

loader = Loader()
config_info = loader.load_config_file()

chunks_per_query = config_info['chunks_per_query']
cppc = config_info['cppc']
push_host = '192.168.2.200:9529'
headers_push = config_info['headers_push']
re_request_interval = config_info['sdk_re_request_interval']


def fake_sdk(
        process_num,
        sdk_no,
        file_size,
        file_id,
        ppc,
        logger,
        start_chunk_id):
    chunk_gross = int(math.ceil(file_size * 1024 * 1024 / int(ppc) / 1392))

    start_time = time.time()
    while start_chunk_id < chunk_gross:
        # send request from here
        if start_chunk_id + chunks_per_query > chunk_gross:
            last_query_chunks = chunk_gross % chunks_per_query
            get_file_url = \
                "http://{0}/push/files/{1}/chunks/{2}_{3}/pieces/{4}".format(
                    push_host, file_id, start_chunk_id, last_query_chunks, cppc)
        else:
            get_file_url = \
                "http://{0}/push/files/{1}/chunks/{2}_{3}/pieces/{4}".format(
                    push_host, file_id, start_chunk_id, chunks_per_query, cppc)
        try:
            send_time = time.time()
            response = urllib2.urlopen(get_file_url)
            receive_time = time.time()
            # 判断sdk下个100ms还是200ms请求数据
            delay = int((receive_time - send_time) * 1000 / 200)
            if response.getcode() == 200:
                logger.logger.info(
                    "200 !Send{send_time}Sleep{sleep_time}-{time}:P{process}-T{thread}:{cid}-{cost}-{fild_id}\n".format(
                        # "200 !Send{send_time}Sleep{sleep_time}-{time}:-T{thread}:{cid}-{cost}-{fild_id}\n".format(
                        time=time.time(),
                        process=process_num,
                        thread=sdk_no,
                        cid=start_chunk_id,
                        cost=time.time() - start_time,
                        fild_id=file_id,
                        send_time=send_time,
                        sleep_time=(delay + 2) * 0.1 - (receive_time - send_time),
                        delay=delay,
                        x=receive_time - send_time))
                start_time = time.time()
                start_chunk_id += chunks_per_query
            time.sleep(max((delay + 2) * 0.1 - (receive_time - send_time), 0))
        except urllib2.HTTPError as e:
            code = e.code
            if code == 503:
                logger.logger.info(
                    "503 !{time}:P{process}-T{thread}:{cid}-{fild_id}\n".
                    # "503 !{time}:-T{thread}:{cid}-{fild_id}\n".
                    format(
                        time=time.time(),
                        process=process_num,
                        thread=sdk_no,
                        cid=start_chunk_id,
                        fild_id=file_id))
                time.sleep(180)
            else:
                logger.logger.info('{0}===========\n'.format(e))
    logger.logger.info('{0}-{1} finish'.format(process_num, sdk_no))
