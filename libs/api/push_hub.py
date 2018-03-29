#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# push-hub related api

from libs.request.http_request import *
from libs.request.header_const import *


def send_download_tasks(ip, port, body):
    uri = "/download_tasks"
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


def send_delete_tasks(ip, port, body):
    uri = "/delete_tasks"
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


if __name__ == "__main__":
    pass