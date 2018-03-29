#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian


from libs.api.push_hub import send_download_tasks

if __name__ == "__main__":
    push_hub_ip = '172.30.0.35'
    push_hub_port = '8001'
    body1 = [
        {
            "file_id": "CA79200718424C8E835BB52B59BA8481",
            "file_url": "http://yunshang.cloutropy.com/demo/hls/ocean_2m/ocean_2mbps.m3u8",
            "file_type": 'm3u8',
            "file_size": 157452256,
            "ppc": 32,
            "cppc": 1,
            "piece_size": 1392,
            "priority": 0,
            "push_ip": "118.190.153.230",
            "push_id": "00:16:3E:06:C3:A6"
        }
    ]

    body2 = [
        {
            "file_id": "588C70A984C84AADAF40DFB600BCD1E0",
            "file_url": "http://c23.myccdn.info/c4332904ab23d9baab43015bb56d4647/5b14e064/mp4/Ocean_2mbps.ts",
            "file_type": 'bigfile',
            "file_size": 172917700,
            "ppc": 32,
            "cppc": 1,
            "piece_size": 1392,
            "priority": 0,
            "push_ip": "118.190.153.230",
            "push_id": "00:16:3E:06:C3:A6"
        }
    ]

    body3 = [
        {
            "file_id": "E27E6CF49CF5441EA66010F87A59FC7D",
            "file_url": "http://yunshang.cloutropy.com/demo/hls/landscape/demo_landscape_10mbps.m3u8",
            "file_type": 'm3u8',
            "file_size": 7128522148,
            "ppc": 240,
            "cppc": 1,
            "piece_size": 1392,
            "priority": 0,
            "push_ip": "118.190.153.230",
            "push_id": "00:16:3E:06:C3:A6"
        }
    ]

    body = body2
    file_size = body[0]["file_size"]
    piece_size = body[0]["piece_size"]
    ppc = body[0]["ppc"]

    block_number = (file_size/4)/(piece_size*ppc)
    print('Total block should be {0}'.format(block_number))

    response = send_download_tasks(push_hub_ip, push_hub_port, body)
