# coding=utf-8
# Author=JKZ
import ConfigParser
import json
import urllib
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import requests
from rediscluster import StrictRedisCluster
# from libs.database.mysql_db import MysqlDB

startup_nodes = [{"host": "172.30.0.20", "port": 6379},
                 {"host": "172.30.0.21", "port": 6379},
                 {"host": "172.30.0.22", "port": 6379}]


def get_login_info_by_ajax(peer_host):
    response = requests.get("http://{0}/ajax/login".format(peer_host))
    result = response.json()
    return result


def get_peer_id_by_ajax(peer_host):
    response = requests.get("http://{0}/ajax/conf".format(peer_host))
    result = response.json().get("peer_id")
    return result


def get_sdk_version_by_ajax(peer_host):
    response = requests.get("http://{0}/ajax/version".format(peer_host))
    result = response.json().get("core")
    return result


def get_seed_ids_from_ini(file_id):
    """
    读取配置文件，返回指定file_id配置的seed_ids
    :param file_id:
    :return:返回类型为list，若未从配置中获取到seed_ids，则返回空列表
    """
    config = ConfigParser.ConfigParser()
    config.readfp(open("seedslist.ini"))
    section_list = config.sections()
    result = list()
    for i in section_list:
        if file_id == config.get(i, "file_id"):
            result = eval(config.get(i, "seed_ids"))
            break

    return result


def get_files_ppc_from_ini(file_id):
    """
    读取配置文件，返回指定file_id对应的ppc
    :param file_id:
    :return: 文件的ppc，若未从配置中获取到ppc，则使用304作为ppc
    """
    config = ConfigParser.ConfigParser()
    config.readfp(open("seedslist.ini"))
    section_list = config.sections()
    result = 304
    for i in section_list:
        if file_id == config.get(i, "file_id"):
            result = eval(config.get(i, "ppc"))
            break

    return result


def get_seed_hosts_from_ini(file_id):
    """
    读取配置文件，返回指定file_id配置的seed_ids对应hosts
    :param file_id:
    :return:
    """
    config = ConfigParser.ConfigParser()
    config.readfp(open("seedslist.ini"))
    section_list = config.sections()
    result = dict()
    for i in section_list:
        if file_id == config.get(i, "file_id"):
            result = eval(config.get(i, "seed_hosts"))
            break

    return result


def get_peer_info_from_redis(peer_ids):
    rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    if type(peer_ids) is not list:
        peer_ids = [peer_ids]
    peer_info_list = list()
    peer_info_keys = ["peer_id", "version", "natType", "publicIP", "publicPort", "privateIP", "privatePort", "stunIP"]
    for peer_id in peer_ids:
        try:
            # 从redis-cluster中获取节点PNIC信息
            pnic = rc.get("PNIC_{0}".format(peer_id))
            pnic = json.loads(pnic)
            peer_info = dict()
            for k in peer_info_keys:
                peer_info[k] = pnic[k]

            # 当播放节点与供源节点使用线上stun探测natType相加≥7无法穿透而播放节点与供源节点又处于同一局域网时，
            # 强行将seedslist中供源节点的natType该为0或1即可使其穿透成功
            # peer_info.update({"natType": 0})

            peer_info_list.append(peer_info)
        except:
            pass

    return peer_info_list


def get_peer_info_by_ajax(peer_hosts):
    if type(peer_hosts) is not list:
        peer_hosts = [peer_hosts]
    peer_info_list = list()
    peer_info_keys = ["natType", "publicIP", "publicPort", "privateIP", "privatePort", "stunIP"]
    for peer_host in peer_hosts:
        # 通过访问ajax获取节点信息
        login_info = get_login_info_by_ajax(peer_host)
        peer_info = dict()
        for k in peer_info_keys:
            peer_info[k] = login_info[k]

        # 当播放节点与供源节点使用线上stun探测natType相加≥7无法穿透而播放节点与供源节点又处于同一局域网时，
        # 强行将seedslist中供源节点的natType该为0或1即可使其穿透成功
        peer_info.update({"natType": 0})

        peer_info["peer_id"] = get_peer_id_by_ajax(peer_host)
        peer_info["version"] = get_sdk_version_by_ajax(peer_host)
        peer_info_list.append(peer_info)

    return peer_info_list


def create_seeds_list(peer_info_list, ppc, cppc=1):
    """
    根据单个或多个seed的节点信息结合ppc，cppc生成seedslist
    :param peer_info_list:
    :param ppc:
    :param cppc:
    :return:
    """
    if type(peer_info_list) is not list:
        peer_info_list = [peer_info_list]
    seeds_list = list()
    for seed in peer_info_list:
        seed.update({"ppc": int(ppc), "cppc": int(cppc)})
        seeds_list.append(seed)
    return seeds_list


# def get_files_ppc_from_mysql():
#     #  从数据库获取所有文件的ppc，返回以file_id为key，以file ppc为value的字典
#     sql = "select hex(file_id),ppc from boss.ppc_tenant_files"
#     files_ppc = dict()
#     resp = MysqlDB().execute(sql).to_rows()
#     for i in resp:
#         files_ppc[i[0]] = i[1]
#
#     return files_ppc


class HttpRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # 引用全局配置，设置seed节点信息的来源为redis或ajax页面
        global seed_source

        if '?' in self.path:
            query = urllib.splitquery(self.path)
            print(query)
            if query[1]:  # 接收get参数
                # 解析参数
                query_params = {}
                for qp in query[1].split('&'):
                    kv = qp.split('=')
                    query_params[kv[0]] = urllib.unquote(kv[1]).decode("utf-8", 'ignore')
                file_id = query_params["fid"]
                # 获取该文件对应的seedslist和ppc的配置
                file_ppc = get_files_ppc_from_ini(file_id)
                if seed_source == "redis":
                    seed_ids = get_seed_ids_from_ini(file_id)
                    seed_info_list = get_peer_info_from_redis(seed_ids)
                elif seed_source == "ajax":
                    seed_hosts = get_seed_hosts_from_ini(file_id)
                    seed_info_list = get_peer_info_by_ajax(seed_hosts)
                else:
                    "Please set the seed source 'redis' or 'ajax', otherwise the seedslist will be a empty list"
                    seed_info_list = []
                seedslist = create_seeds_list(seed_info_list, file_ppc)

                # 返回内容
                body_data = {
                    "seeds": seedslist
                }
                # Just dump data to json, and return it
                print(body_data)
                message = json.dumps(body_data)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(message)


if __name__ == '__main__':
    seed_source = "ajax"  # "redis" or "ajax"
    server = HTTPServer(('0.0.0.0', 80), HttpRequestHandler)
    print('Starting server, use to stop')
    server.serve_forever()

