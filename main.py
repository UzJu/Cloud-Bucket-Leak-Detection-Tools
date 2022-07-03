#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/7/2 14:16
# @File    : main.py

import argparse
from core import main
from config.logs import logger
from config import conf

if __name__ == '__main__':
    print(conf.banner)
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-aliyun', dest='aliyun', help='python3 main.py -aliyun Bucketurl')
        parser.add_argument('-faliyun', dest='faliyun', help='python3 main.py -faliyun filename')
        parser.add_argument('-aws', dest='aws', help='python3 main.py -aws bucketurl')
        args = parser.parse_args()
        if args.aliyun:
            main.aliyun(args.aliyun)
        elif args.faliyun:
            main.aliyun_file_scan(args.faliyun)
        elif args.aws:
            main.AmazoneS3(args.aws)

    except KeyboardInterrupt:
        logger.log("ALERT", "Bye~")
