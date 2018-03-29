#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian


import requests


if __name__ == "__main__":

    url = "http://channel.crazycdn.com/startchannel?user=yunduan&pid=075BCE399A9B464484A59D70E2B0CEAE&url=http://c23.myccdn.info/c4332904ab23d9baab43015bb56d4647/5b14e064/mp4/Ocean_2mbps.ts"

    for i in range(1):
        resp = requests.get(url)
        print(resp.status_code)
        print(resp.content)
