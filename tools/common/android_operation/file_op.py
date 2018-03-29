#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

import optparse
from libs.common.adber import *


if __name__ == "__main__":

    parser = optparse.OptionParser(
        usage="%prog [optons] [<arg1> <arg2> ...]",
        version="1.0"
    )

    parser.add_option('-a', '--action', dest='action', type='string', default="", help='pull/push/delete')
    parser.add_option('-f', '--file', dest='file', type='string', default="", help='conf/meta/data')

    (options, args) = parser.parse_args()
    action = options.action
    file = options.file

    with open('sn.tmp', 'r') as f:
        device_id = f.read()
    print(device_id)

    if action == 'pull':
        src_file = '/sdcard/yunshang/yunshang.{0}'.format(file)
        dest_file = 'yunshang.{0}'.format(file)
        results = adb_pull(device_id, src_file, dest_file)
    elif action == 'push':
        src_file = 'yunshang.{0}'.format(file)
        dest_file = '/sdcard/yunshang/yunshang.{0}'.format(file)
        results = adb_push(device_id, src_file, dest_file)
    elif action == 'delete':
        dest_file = '/sdcard/yunshang/yunshang.{0}'.format(file)
        results = adb_delete(device_id, dest_file)

    print(results)
