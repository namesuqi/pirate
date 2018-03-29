#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 获取linux上ps aux|grep process结果如下
# USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
# root     22798  0.5  0.1 655700  3824 pts/1    Sl   14:49   0:02 ./ys_service_static
# 各字段index参见上面的结果

import time
import subprocess


def linux_shell(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return process.stdout.readlines()

if __name__ == "__main__":
    sdk = 'ys_service'
    command = 'ps aux|grep {0} |grep -v grep'.format(sdk)
    cpu_index = 2
    physical_memory_index = 5

    while True:
        current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 获得返回的列表，包含所有满足条件的行
        results = linux_shell(command)
        result = results[0]  # 只有一个进程，所以是第一个元素
        fields = result.split(' ')
        info = list()
        for field in fields:
            if field:      # 如果不是空串，加到列表中去
                info.append(field)

        # 打印结果，如下形式
        # ('2018-01-30 14:59:57', '0.5', '3852', './ys_service_static\n')
        print(current, info[cpu_index], info[physical_memory_index], info[-1])