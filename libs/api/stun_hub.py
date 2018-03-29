#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

from libs.request.http_request import *
from libs.request.header_const import *


def send_distribute_request(ip, port, body):

    uri = "/distribute_task"
    headers = dict()
    headers.update(content_type_json)
    headers.update(accept_type_json)

    response = send_http_request(
        "POST",
        ip,
        port,
        uri,
        headers,
        None,
        body
    )
    return response


def send_p2p_enable_request(ip, port, body):
    uri = "/p2p_enable"
    headers = dict()
    headers.update(content_type_json)
    headers.update(accept_type_json)

    response = send_http_request(
        'POST',
        ip,
        port,
        uri,
        headers,
        None,
        body
    )
    return response


def send_p2p_disable_request(ip, port, body):
    uri = "/p2p_disable"
    headers = dict()
    headers.update(content_type_json)
    headers.update(accept_type_json)

    response = send_http_request(
        'POST',
        ip,
        port,
        uri,
        headers,
        None,
        body
    )
    return response

if __name__ == "__main__":
    pass