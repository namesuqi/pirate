#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

from libs.api.stun_hub import *

if __name__ == "__main__":
    stun_hub_ip = "172.30.0.25"
    stub_hub_port = "8000"

    body = {"peer_ids": ["0001002396234621864AAA8D206F5B53"]}

    # send_p2p_disable_request(stun_hub_ip, stub_hub_port, body)
    send_p2p_enable_request(stun_hub_ip, stub_hub_port, body)