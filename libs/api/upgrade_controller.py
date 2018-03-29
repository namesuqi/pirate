# coding=utf-8
# Author=JKZ
# upgrade-controller related api

from libs.request.http_request import *
from libs.request.header_const import *


def upgrade_query(ip, port, body):
    uri = "/upgrade_query"
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


def upgrade_rule(ip, port, body):
    uri = "/upgrade_rule"
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

