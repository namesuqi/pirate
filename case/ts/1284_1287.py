# coding=utf-8
# Author=JKZ
import random
import uuid

from libs.api.tracker_srv import send_login, send_control_report

if __name__ == "__main__":
    ts_ip = '172.30.0.18'
    ts_port = '9510'
    # 由MAC地址、当前时间戳、随机数生成peer_id
    peer_id = uuid.uuid1().get_hex().upper()
    login_body = {
       "version": "5.0.1",
       "natType": 0,
       "publicIP": "116.231.59.90",
       "publicPort": 12345,
       "privateIP": "192.168.2.22",
       "privatePort": 12345,
       "stunIP": "118.31.2.166",
       "macs": {}
    }
    control_seed = {
        "file_id": "77BFD961FA87492A860E211E7E5600D2",
        "cppc": 1,
        "download": random.randint(0, 1000000),
        "provide": random.randint(0, 1000000)
    }
    control_channel = {
        "file_id": "77BFD961FA87492A860E211E7E5600D2",
        "type": "vod",
        "chunk_id": random.randint(0, 1000000),
        "cdn": random.randint(0, 1000000),
        "p2p": random.randint(0, 1000000),
        "p2penable": True,
        "err_type": "",
        "op": "del"
    }
    control_body = {
        "peer_id": peer_id,
        "duration": 60,
        "seeds": [],
        "channels": []
    }
    send_login(ts_ip, ts_port, peer_id, login_body)

    # 播放节点control_report
    channel_op_list = ["playing", "add", "del"]
    channel_type_list = ["vod", "download", "hls", "live_flv", "live_m3u8", "live_ts", "push", "vhls", "xmtp"]
    for channel_type in channel_type_list:
        for channel_op in channel_op_list:
            control_channel.update({"type": channel_type, "op": channel_op})
            control_body["channels"] = [control_channel]
            control_body["seeds"] = []
            send_control_report(ts_ip, ts_port, control_body)

    # 供源节点control_report
    control_body["channels"] = []
    control_body["seeds"] = [control_seed]
    send_control_report(ts_ip, ts_port, control_body)


