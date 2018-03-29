# coding=utf-8
# Author=JKZ
from libs.api.upgrade_controller import upgrade_rule, upgrade_query

if __name__ == "__main__":
    upgrade_controller_ip = "172.30.0.30"
    upgrade_controller_port = "9700"
    target_version = "5.0.1"
    # 全量规则（province_ids、user_ids、isp_ids匹配且percent=1）
    specify_upgrade_rule_body = [
        {
            "user_ids": [
                "00000099"
            ],  # 有效user_id（8位16进制字符）列表，可填多个，空列表表示全部用户
            "province_ids": [
                "310000"
            ],  # 有效province_id（6位数字字符）列表，可填多个，空列表表示全部省份
            "isp_ids": [
                "100017"
            ],  # 有效isp_id（6到9位数字字符）列表，可填多个，空列表表示全部isp
            "percent": 1,  # 灰度升级占比（0~1闭区间内任意float数字），不可填多个
            "upgrade_paths": [
                {
                    "core_version": [
                        "4.0.10",
                        "9.9.9"
                    ],
                    "target_version": target_version
                }
            ]  # 升级路径，可填多个，不可为空。"core_version"为二元数组，代表升级范围，单条规则多个core_version之间
            # 不允许有重叠；"target_version"为string，代表目标版本
        }
    ]

    # 全网全量规则（province_ids、user_ids、isp_ids无限制且percent=1）
    universe_upgrade_rule_body = [
        {
            "user_ids": [],
            "province_ids": [],
            "isp_ids": [],
            "percent": 1,
            "upgrade_paths": [
                {
                    "core_version": [
                        "4.0.10",
                        "9.9.9"
                    ],
                    "target_version": target_version
                }
            ]
        }
    ]

    # SDK开机查询请求体
    sdk_without_core_query_body = {"is_basic": "true"}  # basic SDK，无core文件
    sdk_without_ip_query_body = {
        "peer_id": "00000099F69F490194A01E5F79FC34F1",
        "version": "4.2.7",
        "ip_block": "true",
        "public_ip": ""
    }
    sdk_without_ip_query_body_2 = {
        "peer_id": "00000099F69F490194A01E5F79FC34F0",
        "version": "4.2.7",
        "ip_block": "false",
        "public_ip": ""
    }
    sdk_with_ip_query_body = {
        "peer_id": "00000099F69F490194A01E5F79FC34F0",
        "version": "4.2.7",
        "public_ip": "180.173.82.30"
    }

    for upgrade_rule_body in [specify_upgrade_rule_body, universe_upgrade_rule_body]:
        # 配置升级规则
        upgrade_rule(upgrade_controller_ip, upgrade_controller_port, upgrade_rule_body)

        # 发送开机查询请求，并校验返回的版本信息
        for sdk_query_body in [
            sdk_without_core_query_body,
            sdk_without_ip_query_body,
            sdk_without_ip_query_body_2,
            sdk_with_ip_query_body
        ]:
            response = upgrade_query(upgrade_controller_ip, upgrade_controller_port, sdk_query_body)
            # 如果配置的升级规则不是全网全量规则，upgrade-controller向basic SDK返回的target_version为""
            if upgrade_rule_body != universe_upgrade_rule_body and sdk_query_body == sdk_without_core_query_body:
                assert response.json().get("target_version") == ""
            else:
                assert response.json().get("target_version") == target_version


