# coding=utf-8
# Author=JKZ
import uuid


from libs.api.channel_srv import send_start_channel, send_start_hls, send_stop_channel, send_refresh_channel

if __name__ == "__main__":
    channel_srv_ip = "172.30.0.24"
    channel_srv_port = "9665"
    # MySQL中demo用户的peer_prefix和url_prefix对应关系
    # {"user":"demo","peer_prefix":"00000002","url_prefix":"yunshang.cloutropy.com"}
    user = "demo"
    peer_id = "00000002" + uuid.uuid1().get_hex().upper()[:24]
    bigfile_url = "http://yunshang.cloutropy.com/demo/low/Ocean_2mbps.ts"
    media_m3u8_url = "http://yunshang.cloutropy.com/demo/hls/ocean_2m/ocean_2mbps.m3u8"
    master_m3u8_url = "http://yunshang.cloutropy.com/demo/hls/yunshang-master.m3u8"

    # tc-1253
    send_start_channel(channel_srv_ip, channel_srv_port, user, peer_id, bigfile_url)

    # tc-1496
    send_start_hls(channel_srv_ip, channel_srv_port, user, peer_id, media_m3u8_url)
    send_start_hls(channel_srv_ip, channel_srv_port, user, peer_id, master_m3u8_url)

    # tc-1514
    send_stop_channel(channel_srv_ip, channel_srv_port, peer_id, bigfile_url)
    send_stop_channel(channel_srv_ip, channel_srv_port, peer_id, media_m3u8_url)

    # tc-1511
    send_refresh_channel(channel_srv_ip, channel_srv_port, peer_id)

    # tc-1509
    send_refresh_channel(channel_srv_ip, channel_srv_port, peer_id, bigfile_url)
    send_refresh_channel(channel_srv_ip, channel_srv_port, peer_id, media_m3u8_url)

