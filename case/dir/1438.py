# coding=utf-8
# Author=JKZ
import requests
import subprocess
import time


def get_file_duration(filename):
    result = subprocess.Popen(["D:\\ffmpeg-3.3.1-win64-static\\bin\\ffprobe", filename],
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    lines = result.stderr.readlines()
    duration = 0
    for i in lines:
        if "Duration" in i:
            duration = i.split(",")[0][-11:]
    h, m, s = duration.strip().split(":")
    file_duration = int(h)*3600 + int(m)*60 + float(s)

    return file_duration


def calculate_ppc(filesize, duration):
    avg_bitrate = int(filesize)/float(duration)*8
    ppc = int(min(max(16 * round(avg_bitrate/58500/16), 16), 304))
    return ppc


def get_file_size(file_url):
    file_size = None
    retry_times = 5
    while file_size is None and retry_times > 0:
        req_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            # "Connection": "close",
        }
        response = requests.head(file_url, headers=req_headers)
        file_size = response.headers.get("content-length")
        print(file_size)
        retry_times -= 1
        time.sleep(0.5)

    return file_size


if __name__ == "__main__":
    file_url_list = [
                    # "http://yunshang.cloutropy.com/demo/hls/ocean_2m/ocean_2mbps.m3u8",
                    # "http://c23.myccdn.info/e1edddbc239c069d8a2378d9bcd598d6/5b14e012/mp4/Avatar_20Mbps.mp4",
                     "http://c23.myccdn.info/c4332904ab23d9baab43015bb56d4647/5b14e064/mp4/Ocean_2mbps.ts",
                     # "http://c23.myccdn.info/927a6f71a65437d8b1f5dc8edec41224/5b14dfec/mp4/Avatar_15Mbps.mp4",
                     # "http://yunshang.cloutropy.com/demo/hls/ocean_4m/demo_ocean_4mbps.m3u8",
                     # "http://yunshang.cloutropy.com/demo/hls/landscape/demo_landscape_10mbps.m3u8",
                     # "http://yunshang.cloutropy.com/demo/low/Ocean_2mbps.ts",
                     # "http://yunshang.cloutropy.com/demo/middle/demo_11mbps_piano.ts"
    ]

    # from moviepy.editor import VideoFileClip
    # clip = VideoFileClip("http://c23.myccdn.info/c4332904ab23d9baab43015bb56d4647/5b14e064/mp4/Ocean_2mbps.ts")
    # print(clip.duration)

    # for file_url in file_url_list:
    #     print get_file_duration(file_url)
    # print get_file_size(file_url)
    # # file_szie = 1085532904
    # print file_szie, duration
    # print calculate_ppc(file_szie, duration)

    file_url = "http://c23.myccdn.info/c4332904ab23d9baab43015bb56d4647/5b14e064/mp4/Ocean_2mbps.ts"
    duration = get_file_duration(file_url)
    print(duration)
    file_size = get_file_size(file_url)
    print(file_size)
    file_size = 164.91*1024*1024
    ppc = calculate_ppc(file_size, duration)
    print(ppc)





