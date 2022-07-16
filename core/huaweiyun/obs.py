#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/7/15 14:22
# @File    : obs.py

from obs import ObsClient
from config import conf
from config.logs import logger


class HuaWeiCloud_OBS_Check:
    def __init__(self, target, location):
        self.target = target
        self.client = ObsClient(
            access_key_id=conf.huawei_access_key_id,
            secret_access_key=conf.huawei_access_key_key,
            server=f'https://obs.{location}.myhuaweicloud.com'
        )

    def ListObject(self):
        try:
            resp = self.client.listObjects(self.target, max_keys=3)
            for content in resp.body.contents:
                logger.log("INFOR",
                           f"ObjectKey: {content.key}, owner_id: {content.owner.owner_id}, owner_name: {content.owner.owner_name}")
            return True
        except Exception as e:
            logger.log("ALERT", f"BucketName: {self.target}> ListObject权限不足")
            logger.log("ERROR", f"BucketName: {self.target}> ListObject > {repr(e)}")

    def PutObject(self):
        try:
            resp = self.client.putFile(self.target, objectKey="UzJu.html", file_path="./config/UzJu.html")
            if resp['status'] == 403:
                logger.log("ALERT", f"BucketName: {self.target}> PutObject权限不足")
            else:
                logger.log("INFOR", f"BucketName: {self.target}> PutObject成功, 访问UzJu.html查看")
                return True
        except Exception as e:
            logger.log("ERROR", repr(e))

    def GetBucketACL(self):
        try:
            resp = self.client.getBucketAcl(self.target)
            if resp['status'] == 200:
                logger.log("INFOR", f"BucketName: {self.target}> GetBucketACL成功, {resp}")
                return True
            elif resp['status'] == 403:
                logger.log("ALERT", f"BucketName: {self.target}> GetBucketACL权限不足")
        except Exception as e:
            logger.log("ERROR", repr(e))

