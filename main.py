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
from core import DnsResolution
from core import AmazoneCloudS3Bucket

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
        parser.add_argument('-aws', dest='aws', help='python3 -aws UzJu.oss-cn-beijing.aliyuncs.com')
        parser.add_argument('-f', '--file', dest='file', nargs='+', help='python3 -f/--file url.txt')
        args = parser.parse_args()

        '''
        阿里云OSS模块
        '''
        if args.aliyun:
            existDomain = DnsResolution.GetDomainDnsResolution(args.aliyun)
            if existDomain:
                aliyunOss.CheckBucket(existDomain.split(".")[0], existDomain.split(".")[1])
            else:
                getTargetBucket = args.aliyun.split(".")
                aliyunOss.CheckBucket(getTargetBucket[0], getTargetBucket[1])
        '''
        aws S3模块
        '''
        if args.aws:
            '''
            这里本来是这样写的
            bucketDomain = args.aws.split(".")
            但是在Fofa中找资产测试发现一个问题，如果这样写，举个例子
            xxx.xxx.cdn.s3.amazonaws.com
            这种存储桶地址就会取出来
            ['xxx', 'xxx', 'cdn', 's3', 'amazonaws', 'com']
            一般情况下，都能正常取下标来判断xxx就是存储桶名字，但是这里不一样，这里xxx.xxx.cdn都是存储桶的名字，这样取就会存在问题
            
            bucketDomain = args.aws.split(".s3")
            这种写法能解决上述的问题，为什么？
                我们简单分析一下存储桶的地址构造
                xxx.xxx.xxcdn.s3.amazonaws.com
                xxx.xxx.xxcdn.s3.us-east-1.amazonaws.com
                无非就是存储桶名+s3+地区+云厂商的域名 或者 存储桶名+s3+云厂商域名，这里可以用来分割的字段，.s3再适合不过了
            '''
            bucketDomain = args.aws.split(".s3")
            AmazoneCloudS3Bucket.CheckBucket(bucketDomain[0], args.aws)
        if args.file:
            with open(args.file[1], 'r') as f:
                for i in f.read().splitlines():

                    if args.file[0] == "aliyun":
                        existDomain = DnsResolution.GetDomainDnsResolution(i)
                        if existDomain:
                            aliyunOss.CheckBucket(existDomain.split(".")[0], existDomain.split(".")[1])
                        else:
                            getTargetBucket = i.split(".")
                            aliyunOss.CheckBucket(getTargetBucket[0], getTargetBucket[1])

                    elif args.file[0] == "aws":
                        bucketDomain = i.split(".s3")
                        AmazoneCloudS3Bucket.CheckBucket(bucketDomain[0], i)
    except KeyboardInterrupt:
        logger.error("KeyError Out")
