#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：UzJuSecurityTools 
@File    ：main.py
@Author  ：UzJu
@Date    ：2022/2/22 18:19 
@Email   ：UzJuer@163.com
'''
import logging
import sys

import colorlog
import datetime
from config import BannerInfo
import requests
import argparse
from core import aliyunOss

NowTime = datetime.datetime.now().strftime('%Y-%m-%d')

logger = logging.getLogger("mainModule")
log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

# 输出到控制台
console_handler = logging.StreamHandler()
# 输出到文件
file_handler = logging.FileHandler(filename=f'./logs/{NowTime}.log', mode='a', encoding='utf8')

# 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
logger.setLevel(logging.DEBUG)
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.INFO)

# 日志输出格式
file_formatter = logging.Formatter(
    fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
    datefmt='%Y-%m-%d  %H:%M:%S'
)
console_formatter = colorlog.ColoredFormatter(
    fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
    datefmt='%Y-%m-%d  %H:%M:%S',
    log_colors=log_colors_config
)
console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)

# 重复日志问题：
# 1、防止多次addHandler；
# 2、loggername 保证每次添加的时候不一样；
# 3、显示完log之后调用removeHandler
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def initialize(target):
    """
    UserDisable
    错误消息：UserDisable
    问题原因：账号欠费或者由于安全原因，账号被禁用。
    解决方案：请检查账号是否已欠费，或联系技术支持进行安全受限核查。
    """
    try:
        resp = requests.get(f"http://{target}")
        print("Target>>>> ", target)
        print("resp.info>>>> ", resp.text)
        if 'html' in resp.text or 'UserDisable' in resp.text:
            return False
        else:
            return True
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Target: {target}ConnectionError Except INFO: {e}")
        return False


if __name__ == '__main__':
    BannerInfo.echoRandomBannerInfo()
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-aliyun', dest='aliyun', help='python3 -aliyun UzJu.oss-cn-beijing.aliyuncs.com')
        parser.add_argument('-f', '--file', dest='file', help='python3 -f/--file url.txt')
        args = parser.parse_args()
        if args.aliyun:
            getTargetBucket = args.aliyun.split(".")
            aliyunOss.CheckBucket(getTargetBucket[0], getTargetBucket[1])
        if args.file:
            with open(args.file, 'r') as f:
                for i in f.read().splitlines():
                    getTargetBucket = i.split(".")
                    aliyunOss.CheckBucket(getTargetBucket[0], getTargetBucket[1])

    except KeyboardInterrupt:
        logger.error("KeyError Out")
