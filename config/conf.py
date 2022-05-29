#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/2/28 5:18 PM
# @File    : conf.py

# from fake_useragent import UserAgent
# UA = UserAgent(use_cache_server=False)

# headers = {
#     "UserAgent": UA.random
# }
import os
import datetime
import csv

NowTime = datetime.datetime.now().strftime('%Y-%m-%d')
"""
2022年3月6日 16:55
部分用户反馈该库存在报错的问题，故此目前删除该库
最开始使用该库是因为想用HTTP的方式实现功能，所以使用了fake_useragent
现在实现的方式是直接调SDK所以不需要这个Fake_useragent了
"""

# aliyun
AliyunAccessKey_ID = ""
AliyunAccessKey_Secret = ""

# aws
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''


def save_results(target, info):
    headers = ['存储桶地址', '权限']
    filepath = f'{os.getcwd()}/results/{NowTime}.csv'
    rows = [
        [f"{target}", info]
    ]
    if not os.path.isfile(filepath):
        with open(filepath, 'a+', newline='') as f:
            f = csv.writer(f)
            f.writerow(headers)
            f.writerows(rows)
    else:
        with open(filepath, 'a+', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(rows)
