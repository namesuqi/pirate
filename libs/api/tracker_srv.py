# coding=utf-8
# Author=JKZ
# tracker related api

from libs.request.http_request import *
from libs.request.header_const import *


def send_login(ip, port, peer_id, body):
    uri = "/session/peers/" + str(peer_id)
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


def send_heartbeat(ip, port, peer_id):
    uri = "/session/peers/" + str(peer_id)
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


def send_lsm_report(ip, port, peer_id, body):
    uri = "/distribute/peers/" + str(peer_id)
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


def send_control_report(ip, port, body):
    uri = "/sdk/control_report/v1"
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
