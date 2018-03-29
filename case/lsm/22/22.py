# coding=utf-8
# Author=JKZ
import json
import requests

f = open("lsm", 'r')
lsm = json.loads(f.readline())
f.close()

# response = requests.get("http://192.168.1.173:32717/ajax/lsm")
# lsm = response.json()

files = lsm["meta"]["bet"]["files"]
print('fileid   filecrc32    hex')
for i in files:
    file_info = i["file"]
    file_id = file_info["file_id"]
    file_crc32 = file_info["crc32"]
    print file_id, file_crc32, hex(file_crc32).upper()
