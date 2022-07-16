#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/7/15 11:58
# @File    : cos.py

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from config import conf
from config.logs import logger


class TenCent_Cloud_OBS_Check:
    def __init__(self, target, location):
        self.target = target
        config = CosConfig(Region=location, SecretId=conf.tencent_cam_id, SecretKey=conf.tencent_cam_key)
        self.client = CosS3Client(config)

    def ListObject(self):
        try:
            resp = self.client.list_objects(Bucket=self.target)
            if 'Contents' in resp:
                for content in resp['Contents']:
                    logger.log("INFOR", f"ListObject> {content['Key']}")
                return True
        except Exception as e:
            if "Access Denied." in repr(e):
                logger.log("ALERT", f"{self.target}> ListObject权限不足")
            else:
                logger.log("ERROR", repr(e))
            return False

    def PutObject(self):
        try:
            self.client.upload_file(Bucket=self.target,
                                           Key="index.html",
                                           LocalFilePath="./config/UzJu.html",
                                           ACL="public-read",
                                           ContentType="text/html")
            logger.log("INFOR", f"{self.target}> PutObject成功 访问index.html查看结果")
            return True
        except Exception as e:
            if "Access Denied." in repr(e):
                logger.log("ALERT", f"{self.target}> PutObject权限不足")
            else:
                logger.log("ERROR", repr(e))
            return False

    def GetBucketACL(self):
        try:
            resp = self.client.get_bucket_acl(Bucket=self.target)
            logger.log("INFOR", f"{self.target}> GetBucketACL成功, 策略: {resp}")
            return True
        except Exception as e:
            if "Access Denied." in repr(e):
                logger.log("ALERT", f"{self.target}> GetBucketACL权限不足")
            else:
                logger.log("ERROR", repr(e))
            return False
