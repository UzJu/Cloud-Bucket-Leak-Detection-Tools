#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/7/3 13:31
# @File    : results.py

import os
import csv
import pandas as pd
from config.conf import NowTime


def aliyun_save_file(target, BucketHijack, GetBucketObjectList, PutBucketObject, GetBucketAcl, PutBucketAcl,
                     GetBucketPolicy):
    headers = ['Bucket', 'BucketHijack', 'GetBucketObjectList', 'PutBucketObject', 'GetBucketAcl', 'PutBucketAcl',
               'GetBucketPolicy']
    filepath = f'{os.getcwd()}/results/aliyun_{NowTime}.csv'
    rows = [
        [f"{target}", BucketHijack, GetBucketObjectList, PutBucketObject, GetBucketAcl, PutBucketAcl, GetBucketPolicy]
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


def tencent_save_file(target, ListObject, PutObject, GetBucketACL):
    headers = ['Bucket', 'ListObject', 'PutObject', 'GetBucketACL']
    filepath = f'{os.getcwd()}/results/tencentcloud_{NowTime}.csv'
    rows = [
        [f"{target}", ListObject, PutObject, GetBucketACL]
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


def huawei_save_file(target, ListObject, PutObject, GetBucketACL):
    headers = ['Bucket', 'ListObject', 'PutObject', 'GetBucketACL']
    filepath = f'{os.getcwd()}/results/huaweicloud_{NowTime}.csv'
    rows = [
        [f"{target}", ListObject, PutObject, GetBucketACL]
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


def aws_save_file(target, ListObject, PutObject, GetBucketACL):
    headers = ['Bucket', 'ListObject', 'PutObject', 'GetBucketACL']
    filepath = f'{os.getcwd()}/results/aws_{NowTime}.csv'
    rows = [
        [f"{target}", ListObject, PutObject, GetBucketACL]
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
