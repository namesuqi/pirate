# coding=utf-8
# simulate sdk behavior
# author: myn
import time
import math
import urllib2

chunks_per_query = 24
cppc = 1
push_host = '192.168.2.200:9529'


def sdk_download(process_num, sdk_no, file_size, file_id, ppc, logger, start_chunk_id):
    # 计算总的chunk数
    chunk_gross = int(math.ceil(file_size * 1024 * 1024 / int(ppc) / 1392.0))
    start_time = time.time()

    while start_chunk_id < chunk_gross:
        # send request from here
        # 如果下一次请求chunk将超过总chunk数
        if start_chunk_id + chunks_per_query > chunk_gross:
            # 计算最后一个能请求到的chunk
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
            # 使用内置urllib2提高速度
            req = urllib2.Request(get_file_url)
            response = urllib2.urlopen(req)
            receive_time = time.time()
            # 计算接收状态码200后，多久重新发送请求
            sdk_check_interval = 0.2  # SDK每0.2秒检查一下是否收到数据
            delay = int((receive_time - send_time) / sdk_check_interval)
            # 计算需要等待多久，进行下次请求
            sleep_time = (delay + 1) * 0.2 - (receive_time - send_time)
            if response.getcode() == 200:
                logger.logger.info(
                    "200 !Send{send_time}Sleep{sleep_time}-{time}:P{process}-T{thread}:{cid}-{cost}-{fild_id}\n".format(
                        time=time.time(),
                        process=process_num,
                        thread=sdk_no,
                        cid=start_chunk_id,
                        cost=time.time() - start_time,
                        fild_id=file_id,
                        send_time=send_time,
                        sleep_time=sleep_time,
                        delay=delay,
                        x=receive_time - send_time))
                start_time = time.time()
                start_chunk_id += chunks_per_query
            time.sleep(max(sleep_time, 0))
        except urllib2.HTTPError as e:
            code = e.code
            if code == 503:
                logger.logger.info(
                    "503 !{time}:P{process}-T{thread}:{cid}-{fild_id}\n".format(
                        time=time.time(),
                        process=process_num,
                        thread=sdk_no,
                        cid=start_chunk_id,
                        fild_id=file_id))
                time.sleep(60 * 3)
            else:
                logger.logger.info('error{0}'.format(e.code))
    logger.logger.info('{0} finish'.format(file_id))
