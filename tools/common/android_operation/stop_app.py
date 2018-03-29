#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 启动或者停止android app


from libs.common.adber import *


if __name__ == "__main__":
    with open('sn.tmp', 'r') as f:
        device_id = f.read()
    print(device_id)
    command = 'am force-stop com.cloutropy.bplayer'
    results = adb_shell(device_id, command)
    print(results)