#!/usr/bin/env python
# coding=utf-8
# author: Tang Hong
# 生成不同isp和province的数据
# 格式：{isp_province1:[pid_1, ], isp_province2:[pid_n, ], ...}

import inspect
import random
import json
import os
import sys


def random_peer_ids(peer_num, isp_province, prefix):
    '''
    产生一组随机的peer_id列表
    :param peer_num: 生成多少个
    :param isp_province:
    :param prefix:
    :return:
    '''
    chars = "1234567890ABCDEF"
    peer_list = list()
    isp_peers = dict()
    assert len(str(prefix)) == 8
    for num in range(peer_num):
        ids = list()
        for char in range(4):
            ids.append(random.choice(chars))
        pid_ids = ''.join(ids)  # 4位的随机串
        peer_id = str(prefix) + "0"*20 + pid_ids
        peer_list.append(peer_id)
    isp_peers[isp_province] = peer_list
    return isp_peers


if __name__ == "__main__":
    peer_ids_1 = random_peer_ids(20, "100017_310000", "BBBBBBBB")
    peer_ids_2 = random_peer_ids(20, "100026_410000", "CCCCCCCC")
    peer_ids_3 = random_peer_ids(20, "000000_500000", "DDDDDDDD")
    peer_ids_info = dict(peer_ids_1.items()+peer_ids_2.items()+peer_ids_3.items())
    print peer_ids_info
    # get current dir path
    file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
    parent_path = os.path.dirname(file_path)
    f = open('{0}/peer_ids.txt'.format(parent_path), 'w')
    f.write(json.dumps(peer_ids_info))
    f.close()
