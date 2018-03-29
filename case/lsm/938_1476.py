#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian


from libs.api.stun_hub import *


if __name__ == "__main__":
    stun_hub_ip = "172.30.0.25"
    stub_hub_port = "8000"

    # 删除已经下载的文件
    body = [
        {
            "file_id": "011AF9DA247941F9B2A8AE81DC72EB5E",
            "operation": "delete",
            "peer_id": "0001002396234621864AAA8D206F5B53"
        }
    ]

    send_distribute_request(stun_hub_ip, stub_hub_port, body)


