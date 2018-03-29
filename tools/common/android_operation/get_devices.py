#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 获得当前工作机连接的device id


from libs.common.commander import run


if __name__ == "__main__":
    device_ids = list()
    command = 'adb devices'
    results = run(command)
    for result in results:
        # 找到device字符串，但是不包含devices字符串
        # 因为第一行有可能是List of devices attached
        if result.find('device') != -1 and result.find('devices') == -1:
            device_ids.append(result.split()[0])
    print(device_ids)

    with open('sn.tmp', 'w') as f:
        f.write(device_ids[0])