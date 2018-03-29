#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian


from libs.api.stun_hub import *


if __name__ == "__main__":
    stun_hub_ip = "172.30.0.25"
    stub_hub_port = "8000"

    # delete task
    body = [
        {
            "file_id": "588C70A984C84AADAF40DFB600BCD1E0",
            "operation": "download",
            "file_size": 172917700,
            "piece_size": 1392,
            "ppc": 32,
            "cppc": 1,
            "chunk_num": 4,
            "priority": 1,
            "push_port": 80,
            "push_ip": "118.190.153.230",
            "peer_id": "0001002396234621864AAA8D206F5B53"
        }
    ]

    body2 = [
        {
            "file_id": "588C70A984C84AADAF40DFB600BCD1E0",
            "operation": "delete",
            "peer_id": "0001002396234621864AAA8D206F5B53"
        },
        {
            "file_id": "CA79200718424C8E835BB52B59BA8481",
            "operation": "download",
            "file_size": 157452256,
            "piece_size": 1392,
            "ppc": 32,
            "cppc": 1,
            "chunk_num": 4,
            "priority": 1,
            "push_port": 80,
            "push_ip": "118.190.153.230",
            "peer_id": "0001002396234621864AAA8D206F5B53"
        }
    ]

    send_distribute_request(stun_hub_ip, stub_hub_port, body2)


