#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/7/2 19:57
# @File    : aws.py

from boto3.session import Session
from config.logs import logger
from config import conf


class Amazone_Cloud_S3Bucket_Check:
    def __init__(self, target, location):
        """

        :desc: Aws class init
        :param BucketName: aws bucket name
        :param BucketDomain: aws bucket region
        """
        self.getBucketName = target
        self.getBucketDomain = location
        session = Session(aws_access_key_id=conf.AWS_ACCESS_KEY,
                          aws_secret_access_key=conf.AWS_SECRET_KEY)
        self.s3 = session.client('s3')
        self.s3_resource = session.resource('s3')

    def Check_Bucket_ListObject(self):
        try:
            getObjectList = self.s3_resource.Bucket(self.getBucketName)
            for getObject in getObjectList.objects.all():
                logger.log("INFOR", f"List Bucket Object > {getObject.key}")
                break
            return True
        except Exception as e:
            if "NoSuchBucket" in str(e):
                logger.log("ALERT", "NoSuchBucket")
            else:
                logger.log("ERROR", repr(e))

    def Check_Bucket_PutObject(self):
        try:
            self.s3_resource.Object(self.getBucketName, "UzJu.html").put(
                Body="Put By https://github.com/UzJu/Cloud-Bucket-Leak-Detection-Tools.git",
                ContentType='text/html')
            logger.log("INFOR", f"Put File Success > {self.getBucketDomain}/UzJu.html")
            return True
        except Exception as e:
            logger.log("ERROR", repr(e))
            return False

    def Check_Bucket_GetBucketAcl(self):
        try:
            response = self.s3.get_bucket_acl(Bucket=self.getBucketName)
            logger.log("INFOR", f"Get Bucket Acl Success > {response}")
            return True
        except Exception as e:
            logger.log("ERROR", repr(e))
            return False



