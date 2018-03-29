# coding=utf-8
# Author=JKZ
import uuid

from libs.api.tracker_srv import send_login, send_heartbeat

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

    send_login(ts_ip, ts_port, peer_id, login_body)
    send_heartbeat(ts_ip, ts_port, peer_id)
    file_status_list = ["downloading", "done", "waiting", "interrupt", "deleted", None]
