#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 获取android上top结果如下
# PID PR CPU% S  #THR     VSS     RSS PCY UID      Name
# 727  5   0% S    55 195108K  17116K  tv media    /system/bin/mediaserver
# 各字段index参见上面的结果

import time
from libs.common.adber import *


if __name__ == "__main__":
    device_id = 'B5VD63N1S6'
    command = '"top -n 1 |grep com.cloutropy.bplayer:monitor"'
    cpu_index = 2
    physical_memory_index = 6

    while True:
        current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 获得返回的列表，包含所有满足条件的行
        results = adb_shell(device_id, command)
        result = results[0]  # 只有一个进程，所以是第一个元素
        fields = result.split(' ')
        info = list()
        for field in fields:
            if field:      # 如果不是空串，加到列表中去
                info.append(field)

        # 打印结果，如下形式
        # ('2018-01-30 14:36:49', '0%', '62404K', 'com.cloutropy.bplayer:monitor\r\r\n')
        print(current, info[cpu_index], info[physical_memory_index], info[-1])