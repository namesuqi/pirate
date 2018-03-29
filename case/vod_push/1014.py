#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

from libs.api.push_hub import send_delete_tasks

if __name__ == "__main__":
    push_hub_ip = '172.30.0.35'
    push_hub_port = '8001'
    body = [
        {
            "file_id": "CA79200718424C8E835BB52B59BA8481",
            "priority": 0,
            "push_ip": "118.190.153.230",  # 该IP为该vod-push探测出的IP
            "push_id": "00:16:3E:06:C3:A6"
        }
    ]

    send_delete_tasks(push_hub_ip, push_hub_port, body)
