#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian


import requests
stun_hub_ip = '172.30.0.25'
distribute_task_url = "http://{0}:8000/distribute_task".format(stun_hub_ip)


if __name__ == "__main__":
    body = list()

    body.append(
        dict(file_id='A79DE5F5C45443F7B6780DA0AF1C2425', operation="download", file_size=172917700, piece_size=1392,
             ppc=32, cppc=1, priority=1, push_port=80, push_ip='118.190.153.230', peer_id='0001002373BA4FCFBEF1059A844ABEBA')
    )
    resp = requests.post(distribute_task_url, json=body)
    print(resp.status_code)
    print(resp.content)
