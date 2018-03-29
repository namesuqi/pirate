#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 发送master文件的start_hls请求


from libs.api.channel_srv import *


if __name__ == "__main__":
    channel_srv_ip = "172.30.0.24"
    channel_srv_port = 9665
    user_id = "demo"
    peer_id = "00010023D2224901BFD29D0CEA50EEEF"
    url = "http://yunshang.cloutropy.com/demo/hls/yunshang-master.m3u8"

    send_start_hls(channel_srv_ip, channel_srv_port, user_id, peer_id, url)

