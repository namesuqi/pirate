# coding=utf-8
# author: zengyuetian
# start sdk on local machine
# 本文件夹中放置你的SDK静态包
# 支持start，stop，restart
# 标准用法 python local_main.py --num SDKNUM --action start --prefix 0x00010048 --lsm 500

import os
import time

SDK_FILE = 'ys_service_static'
SDK_PORT_STEP = 10
SDK_PORT_START = 30000

USE_LF_PREFIX = ""
# USE_LF_PREFIX = " -x 075BCE73 "

# 要使用的雷锋前缀，暂时无用
# USER_PREFIX = ""
USER_PREFIX = " -u 0x00010048 "

# 分散启动，避免burst
START_INTERVAL = 2

# LSM缓存大小，可以通过参数传入
LSM = 500
#DEBUG_TAG = ""
DEBUG_TAG = "TCMALLOC_PAGE_FENCE=true"


def stop_player():
    print "stop player"
    os.system(" ps aux | grep flv_play.py |grep -v grep |awk -F ' ' '{print $2}' | xargs kill -9")


def stop_sdk():
    print "stop sdk"
    os.system(" ps aux | grep ys_service_static |grep -v grep |awk -F ' ' '{print $2}' | xargs kill -9")


def create_folder(start, end):
    print "recreate_sdk_folder from {start} to {end}".format(start=start, end=end)
    os.system("chmod +x ./{sdk}".format(sdk=SDK_FILE))
    for i in range(start, end):
        os.system("rm -rf ./{dir}".format(dir=i))
        os.system("mkdir -p ./{dir}".format(dir=i))
        os.system("cp ./{sdk}  ./{dir}/".format(sdk=SDK_FILE, dir=i))
        os.system("cp -r ./conf  ./{dir}/".format(dir=i))


def start_sdk(start, end):
    print "start sdk for {start} to {end}".format(start=start, end=end)
    for i in range(start, end):
        port = i * SDK_PORT_STEP + SDK_PORT_START
        p2pclient = "ulimit -c unlimited && cd {dir} && {debug_tag} nohup ./{sdk}".format(dir=i, sdk=SDK_FILE, debug_tag=DEBUG_TAG)
        cmd = "{command} -p {port} -q {lsm} {use_lf} {peer_user} > /dev/null 2>&1 &".format(
            command=p2pclient, port=port, lsm=LSM, use_lf=USE_LF_PREFIX, peer_user=USER_PREFIX)
        # cmd = "{command} -p {port} -q {lsm} {use_lf} {peer_user} > /home/admin/vod/{dir}/console.log 2>&1 &".format(
        #     command=p2pclient, port=port, lsm=LSM, use_lf=USE_LF_PREFIX, peer_user=USER_PREFIX, dir=i)
        print cmd
        os.system(cmd)
        time.sleep(START_INTERVAL)


def start_player(start, end, url):
    print "start player for {start} to {end}".format(start=start, end=end)
    for i in range(start, end):
        port = i * SDK_PORT_STEP + SDK_PORT_START

        # url = "http://127.0.0.1:{port}/live_flv/user/wasu?url=http://test.live.entropycode.net/live/test3.flv" \
        #     .format(port=port)

        channel_url = "http://127.0.0.1:{port}/live_flv/user/xmtv?url={url}" \
            .format(port=port, url=url)
        cmd = "nohup python flv_play.py {url} > /dev/null 2>&1 &".format(url=channel_url)
        print cmd
        os.system(cmd)
        time.sleep(START_INTERVAL)


def start_vod_player(start, end, url):
    print "start player for {start} to {end}".format(start=start, end=end)

    # 首先把以前的{port}.run文件删除
    for i in range(start, end):
        port = i * SDK_PORT_STEP + SDK_PORT_START
        os.system('rm -f {0}.run'.format(port))
        time.sleep(0.01)

    time.sleep(1)  # 等待文件确实被删除
    # 外部是一个循环，用于检查是否某些端口播放完成，需要再次播放
    # 如果端口文件{port}.run不存在，表示该端口播放完成，可以启动
    # 如果端口文件存在，那么就等下一次的检查
    while True:
        for i in range(start, end):
            port = i * SDK_PORT_STEP + SDK_PORT_START

            # url = "http://127.0.0.1:{port}/live_flv/user/wasu?url=http://test.live.entropycode.net/live/test3.flv" \
            #     .format(port=port)
            if not os.path.exists('{0}.run'.format(port)):
                channel_url = "http://127.0.0.1:{port}/live_flv/user/xmtv?url={url}" \
                    .format(port=port, url=url)
                cmd = "nohup python flv_play.py {url} > /dev/null 2>&1 &".format(url=channel_url)
                print cmd
                os.system(cmd)
            time.sleep(START_INTERVAL)
    time.sleep(60)


if __name__ == "__main__":

    import optparse

    parser = optparse.OptionParser(
        usage="%prog [optons] [<arg1> <arg2> ...]",
        version="1.0"
    )
    parser.add_option('-n', '--num', dest='num', type='int', default=10, help='how many sdk to start')
    parser.add_option('-a', '--action', dest='action', type='string', default="", help='restart or start')
    parser.add_option('-l', '--lsm', dest='lsm', type='int', default=500, help='lsm quota')
    parser.add_option('-p', '--prefix', dest='prefix', type='string', default="", help='peer id prefix')
    parser.add_option('-u', '--url', dest='url', type='string', default="", help='channel url')

    (options, args) = parser.parse_args()
    num = options.num
    action = options.action
    lsm = options.lsm
    prefix = options.prefix
    url = options.url

    # set variables
    USER_PREFIX = " -u {0} ".format(prefix)
    LSM = lsm
    # print for debugging
    print "sdk num is:", num
    print "action is:", action
    print "lsm is:", lsm
    print "prefix is:", prefix

    SDK_START = 0
    SDK_END = SDK_START + num

    if action != "start_play":
        # stop sdk
        stop_sdk()
        time.sleep(1)

        if action == "stop":
            exit(0)

        if action == "start":
            # create folders
            create_folder(SDK_START, SDK_END)
            time.sleep(1)

        # start sdk
        start_sdk(SDK_START, SDK_END)
        time.sleep(1)
    else:
        start_vod_player(SDK_START, SDK_END, url)




