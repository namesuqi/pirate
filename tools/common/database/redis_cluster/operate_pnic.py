#!/usr/bin/env python
# coding=utf-8
# __author__ = 'liwenxuan'
# 写入PNIC到Redis-cluster; 删除指定前缀的所有pnic

from rediscluster import StrictRedisCluster
import json
import time
import threading

# ---------------------------------------------------------------------------------------------------------------------

REDIS_CLUSTER_HOST = ["172.30.0.20", "172.30.0.21", "172.30.0.22"]
REDIS_CLUSTER_PORT = [6379, 6379, 6379]

# ---------------------------------------------------------------------------------------------------------------------


def connect_to_redis_cluster():
    startup_nodes = [{"host": host, "port": port} for host, port in zip(REDIS_CLUSTER_HOST, REDIS_CLUSTER_PORT)]
    return StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

# -------------------------------------------------------------------------------------------------------------

# redis-cluster
peer_info = {
    # "peer_id": peer_id,
    "version": "4.5.0",
    "natType": 4,
    "publicIP": "192.168.1.1",
    "publicPort": 80,
    "privateIP": "192.168.1.1",
    "privatePort": 80,
    "province_id": "310000",
    "isp_id": "100017",
    "city_id": "310100",
    "country": "CN",
    "stunIP": "192.168.2.7",
    "ssid": "F"*32,
    # "history": [1517399588]
}


def add_pnic(redis_cluster, prefix, peer_count, peer_start=1, ttl=None, **other_fields):
    assert len(str(prefix)) == 8
    peer_info.update(other_fields)
    for i in xrange(int(peer_start), int(peer_count)+int(peer_start)):
        peer_id = str(prefix) + "F"*8 + str(i).zfill(16)
        peer_info["peer_id"] = peer_id
        if ttl is None:
            redis_cluster.set("PNIC_"+peer_id, json.dumps(peer_info))
        else:
            redis_cluster.setex("PNIC_"+peer_id, int(ttl), json.dumps(peer_info))
        # if i % 10000 == 0:
        #     print "set", peer_id, ":", peer_info
    print "add", peer_count, "pnic"


def delete_pnic(redis_cluster, *prefix):
    for x in prefix:
        keys = redis_cluster.keys("PNIC_"+str(x)+"*")
        for k in keys:
            redis_cluster.delete(k)
            # print "delete key:", k
        print "delete", len(keys), "pnic"

# ---------------------------------------------------------------------------------------------------------------------


def multi_thread_add_pnic(pnic_count, thread_number, prefix="F"*8, peer_start=1, ttl=None):
    """
    通过多线程写入大量pnic时用
    :param pnic_count: 需要写入的pnic的总量
    :param thread_number: 线程数
    :param prefix: peer_id的八位前缀
    :param ttl: pnic的过期时间, 默认为不会过期
    :return:
    """
    rc = connect_to_redis_cluster()
    item_num = float(pnic_count)/float(thread_number)
    threads = list()
    start_time = time.time()
    for i in range(thread_number):
        t = threading.Thread(target=add_pnic, args=(rc, prefix, item_num, int(peer_start)+item_num*i, ttl))
        t.setDaemon(True)
        threads.append(t)
        t.start()
    for thr in threads:
        thr.join()
    end_time = time.time()
    print("cost {0} seconds to finish {1} items".format(end_time-start_time, pnic_count))

# ---------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    multi_thread_add_pnic(100000, 10)

