#!/usr/bin/env python
# coding=utf-8
# author: mao yu nan

# record SDKs behavior
import logging


class Log(object):
    def __init__(self, log_name, log_address, level=logging.DEBUG):
        self.logger = logging.getLogger(log_name)
        formatter = logging.Formatter('%(message)s')
        file_handler = logging.FileHandler(log_address)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(level)
