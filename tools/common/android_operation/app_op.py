#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# android app操作

import optparse
from libs.common.adber import *


if __name__ == "__main__":
    parser = optparse.OptionParser(
        usage="%prog [optons] [<arg1> <arg2> ...]",
        version="1.0"
    )

    parser.add_option('-a', '--action', dest='action', type='string', default="", help='install/uninstall/start/stop/peer_id')

    (options, args) = parser.parse_args()
    action = options.action

    with open('sn.tmp', 'r') as f:
        device_id = f.read()
    print(device_id)

    if action == 'install':
        results = adb_install(device_id, 'aplayer.apk')
    elif action == 'uninstall':
        results = adb_uninstall(device_id, 'com.cloutropy.bplayer')
    elif action == 'start':
        command = 'am start com.cloutropy.bplayer/.MainActivity'
        results = adb_shell(device_id, command)
    elif action == 'stop':
        command = 'am force-stop com.cloutropy.bplayer'
        results = adb_shell(device_id, command)
    print(results)

