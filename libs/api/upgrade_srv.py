# coding=utf-8
# Author=JKZ
# upgrade-srv related api

from libs.request.http_request import *
from libs.request.header_const import *


def upgrade_get(ip, port, body):
    uri = "/upgrade_get"
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


def upgrade_add(ip, port, body):
    uri = "/upgrade_add"
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

