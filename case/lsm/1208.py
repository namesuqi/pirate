#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian


from libs.api.stun_hub import *


if __name__ == "__main__":
    stun_hub_ip = "172.30.0.25"
    stub_hub_port = "8000"

    # delete task
    file_info = {
            "file_id": "E27E6CF49CF5441EA66010F87A59FC7D",
            "operation": "delete",
            "peer_id": "0001002396234621864AAA8D206F5B53"
        }
    body = [file_info for i in range(6)]

    send_distribute_request(stun_hub_ip, stub_hub_port, body)


