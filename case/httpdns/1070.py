#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

from libs.database.etcd_handler import *

if __name__ == "__main__":
    # 需要根据当前实际配置修改
    ttl_conf_old = {"report.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
                 "channel.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
                 "upgradev2.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
                 "opt.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
                 "hls.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
                 "stats.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
                 "seeds.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
                 "vodtest.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 300},
                 "stun2.crazycdn.com": {"ips": {"default": ["118.190.148.163"]}, "ttl": 1800},
                 "live-ch.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
                 "ts.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
                 "control.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800},
                 "errlogs.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 1800}}

    # print(read_etcd_key('/business/httpdns/v2/domain_ip_map/default'))

    ttl_conf_1 = {"report.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 300},
                    "channel.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 300},
                    "upgradev2.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 300},
                    "opt.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 300},
                    "hls.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 300},
                    "stats.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 300},
                    "seeds.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 300},
                    "vodtest.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 300},
                    "stun2.crazycdn.com": {"ips": {"default": ["118.190.148.163"]}, "ttl": 300},
                    "live-ch.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 300},
                    "ts.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 300},
                    "control.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 300},
                    "errlogs.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 300}}



    set_etcd_key('default', ttl_conf_old, '/business/httpdns/v2/domain_ip_map/')