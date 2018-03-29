#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

from libs.database.etcd_handler import *


def enable_p2p_switch(user_prefix):
    set_etcd_key(user_prefix, '100', '/business/ops/sdk/p2p/users/')

def disable_p2p_switch(user_prefix):
    set_etcd_key(user_prefix, '0', '/business/ops/sdk/p2p/users/')

if __name__ == "__main__":
    pass