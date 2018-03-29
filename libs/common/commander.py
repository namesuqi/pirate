# coding=utf-8
# author: zengyuetian
# subprocess command wrapper


import subprocess


def run(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return process.stdout.readlines()