#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian


from libs.api.stun_hub import *


if __name__ == "__main__":
    stun_hub_ip = "172.30.0.25"
    stub_hub_port = "8000"

    # 选一个大一点的文件
    body = [
        {
            "file_id": "CD257E94C2BA48B2A2F045D3F5ABEB72",
            "operation": "download",
            "file_size": 1085532904,
            "piece_size": 1392,
            "ppc": 256,
            "cppc": 1,
            "chunk_num": 4,
            "priority": 1,
            "push_port": 80,
            "push_ip": "118.190.153.230",
            "peer_id": "0001002396234621864AAA8D206F5B53"
        }
    ]

    send_distribute_request(stun_hub_ip, stub_hub_port, body)


