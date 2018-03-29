# coding=utf-8
# Author=JKZ
import uuid

from libs.api.tracker_srv import send_login, send_lsm_report

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
    lsm_file = {
        "file_id": "0205372A6B31469BAB0683BE37F0B2F3",
        "ppc": 304,
        "cppc": 1,
        "psize": 1392,
        "fsize": 775134238,
        "percent": 100,
        "stat": "interrupt"
    }
    lsm_body = {
        "lsmTotal": 209715200,
        "lsmFree": 206524016,
        "diskTotal": 40212119552,
        "diskFree": 23363497984,
        "universe": True,  # True表示为全量汇报
        "files": []
    }
    send_login(ts_ip, ts_port, peer_id, login_body)

    # 全量汇报，文件数≤1
    file_status_list = ["downloading", "done", "waiting", "interrupt", None]
    for file_status in file_status_list:
        # file_status为None时全量汇报无文件信息
        if file_status is not None:
            lsm_file.update({"stat": file_status})
            lsm_body["files"] = [lsm_file]
        send_lsm_report(ts_ip, ts_port, peer_id, lsm_body)

    # 全量汇报，文件数＞1
    lsm_file2 = lsm_file.copy()
    lsm_file2.update({"file_id": uuid.uuid1().get_hex().upper()})
    lsm_body["files"] = [lsm_file, lsm_file2]
    send_lsm_report(ts_ip, ts_port, peer_id, lsm_body)

