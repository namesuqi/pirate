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

    ttl_conf_1 = {"report.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 90},
                    "channel.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 90},
                    "upgradev2.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 90},
                    "opt.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 90},
                    "hls.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 90},
                    "stats.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 90},
                    "seeds.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 90},
                    "vodtest.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 90},
                    "stun2.crazycdn.com": {"ips": {"default": ["118.190.148.163"]}, "ttl": 90},
                    "live-ch.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 90},
                    "ts.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 90},
                    "control.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 90},
                    "errlogs.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 90}}

    ttl_conf_2 = {"report.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 230},
                  "channel.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 240},
                  "upgradev2.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 250},
                  "opt.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 130},
                  "hls.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 140},
                  "stats.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 150},
                  "seeds.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 160},
                  "vodtest.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 170},
                  "stun2.crazycdn.com": {"ips": {"default": ["118.190.148.163"]}, "ttl": 180},
                  "live-ch.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 190},
                  "ts.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 200},
                  "control.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 210},
                  "errlogs.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 220}}

    ttl_conf_3 = {"report.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 120},
                  "channel.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 120},
                  "upgradev2.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 120},
                  "opt.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 120},
                  "hls.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 120},
                  "stats.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 120},
                  "seeds.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 120},
                  "vodtest.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 120},
                  "stun2.crazycdn.com": {"ips": {"default": ["118.190.148.163"]}, "ttl": 120},
                  "live-ch.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 120},
                  "ts.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 120},
                  "control.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 120},
                  "errlogs.crazycdn.com": {"ips": {"default": ["47.104.178.217"]}, "ttl": 120}}

    set_etcd_key('default', ttl_conf_old, '/business/httpdns/v2/domain_ip_map/')