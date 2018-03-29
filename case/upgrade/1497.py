# coding=utf-8
# Author=JKZ
from libs.api.upgrade_srv import upgrade_get, upgrade_add

if __name__ == "__main__":
    upgrade_srv_ip = "172.30.0.30"
    upgrade_srv_port = "9540"
    add_body = {
        "version": "9.9.9",  # 版本号，必选
        "os": "linux",  # 操作系统类型，必选
        "distribution": "ubuntu",  # 操作系统发行版，必选
        "envCPU": "x86_64",  # cpu，必选
        "toolchain": "nocheck",  # 工具链，必选
        "md5": "74a3a21ffca9b09d8d1f90a54a3014ca",  # 文件MD5，必选
        "url": "upgrade/4.1.0/linux/ubuntu/x86_64/nocheck/libys-core.4.1.0.so"  # 文件下载url,必选
    }

    get_body = {
        "targetversion": "9.9.9",  # 目标版本，必选
        "peerid": "0000000418874D798552C9AF05CE55B0",  # peer id， 可选
        "shellversion": "1.0.1",  # shell版本，必选
        "os": "linux",  # 操作系统类型，必选
        "osversion": "1.0.1",  # 操作系统版本，必选
        "distribution": "ubuntu",  # 操作系统发行版，必选
        "distributionversion": "1.0.1",  # 发行版版本，必选
        "envCPU": "x86_64",  # cpu，必选
        "realCPU": "x86_64",  # ，必选
        "toolchain": "nocheck"  # 工具链，必选
    }
    response = upgrade_add(upgrade_srv_ip, upgrade_srv_port, add_body)
    errcode = response.json().get("errcode")
    assert errcode == ""

    response = upgrade_get(upgrade_srv_ip, upgrade_srv_port, get_body)
    assert response.json().get("md5") == add_body["md5"]

