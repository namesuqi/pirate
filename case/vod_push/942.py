#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

import requests

if __name__ == "__main__":
    push_ip = "172.30.0.32"
    push_port = 9529
    file_id = "805AD6CDAAFB455BB54967DC394AD891"
    url = "http://{0}:{1}/push/files/{2}/chunks/0_12/pieces/1".format(push_ip, push_port, file_id)
    for i in range(1):
        print(i)
        resp = requests.get(url)
    print(resp.status_code)
    print(resp.headers)
