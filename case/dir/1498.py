#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 发送media文件的start_hls请求


from libs.api.channel_srv import *


def get_m3u8_duration(file_name):
    """
    获取m3u8视频文件的总时长
    :param file_name:
    :return:
    """
    duration = 0
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("#EXTINF:"):
                # 内容形如"#EXTINF:10.260256,"   所以掐头去尾
                dt = (line.strip()[8:-1])
                duration += float(dt)
    print(duration)
    return duration


def calculate_ppc(file_size, duration):
    avg_bitrate = int(file_size) / float(duration) * 8
    ppc = int(min(max(16 * round(avg_bitrate / 58500 / 16), 16), 304))
    return ppc


if __name__ == "__main__":
    channel_srv_ip = "172.30.0.24"
    channel_srv_port = 9665
    user_id = "demo"
    peer_id = "00010023D2224901BFD29D0CEA50EEEF"
    url = "http://yunshang.cloutropy.com/demo/hls/ocean_2m/ocean_2mbps.m3u8"

    send_start_hls(channel_srv_ip, channel_srv_port, user_id, peer_id, url)
    file_size = 157452256
    file_duration = get_m3u8_duration("ocean_2mbps.m3u8")
    ppc = calculate_ppc(file_size, file_duration)
    print("ppc:{0}".format(ppc))
