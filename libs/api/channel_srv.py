# coding=utf-8
# Author=JKZ
# channel_srv related api

from libs.request.http_request import *
from libs.request.header_const import *


def send_start_channel(ip, port, user_name, peer_id, channel_url):
    uri = "/startchannel?user=" + str(user_name) + "&pid=" + str(peer_id) + "&url=" + str(channel_url)
    headers = dict()
    headers.update(content_type_json)
    headers.update(accept_type_json)
    response = send_http_request(
        "GET",
        ip,
        port,
        uri,
        headers,
        None,
        None
    )
    return response


def send_start_hls(ip, port, user_name, peer_id, channel_url):
    uri = "/starthls?pid=" + str(peer_id) + "&user=" + str(user_name) + "&url=" + str(channel_url)
    headers = dict()
    headers.update(content_type_json)
    headers.update(accept_type_json)
    response = send_http_request(
        "GET",
        ip,
        port,
        uri,
        headers,
        None,
        None
    )
    return response


def send_stop_channel(ip, port, peer_id, channel_url):
    uri = "/stopchannel?pid=" + str(peer_id) + "&url=" + str(channel_url)
    headers = dict()
    headers.update(content_type_json)
    headers.update(accept_type_json)
    response = send_http_request(
        "GET",
        ip,
        port,
        uri,
        headers,
        None,
        None
    )
    return response


def send_refresh_channel(ip, port, peer_id, channel_url=None):
    if channel_url is None:
        uri = "/refreshchannel?pid=" + str(peer_id)
    else:
        uri = "/refreshchannel?pid=" + str(peer_id) + "&url=" + str(channel_url)
    headers = dict()
    headers.update(content_type_json)
    headers.update(accept_type_json)
    response = send_http_request(
        "GET",
        ip,
        port,
        uri,
        headers,
        None,
        None
    )
    return response
