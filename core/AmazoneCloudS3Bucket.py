#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/4/7 15:33
# @File    : AmazoneCloudS3Bucket.py
import botocore
from boto3.session import Session
import boto3
from config import conf
import logging
import datetime

module_logger = logging.getLogger("mainModule.AmazoneCloudS3Bucket")
NowTime = datetime.datetime.now().strftime('%Y-%m-%d')


class AwsCloudS3Check:
    def __init__(self, BucketName, BucketDomain):
        '''
        bucketName: 只取Bucket名字
        BucketDomain: Bucket完整域名
        '''
        self.getBucketName = BucketName
        self.getBucketDomain = BucketDomain

        '''
        Boto3 Session 和 Client
        '''
        session = Session(aws_access_key_id=conf.AWS_ACCESS_KEY,
                          aws_secret_access_key=conf.AWS_SECRET_KEY)
        self.s3 = session.client('s3')

        '''
        为了解决boto3 Clinet中没有resource的问题
        因为如果使用client, 在调用CheckBucketListObject的时候, 会提示没有Object
        '''
        self.s3_resource = session.resource('s3')
        '''
        Logger
        '''
        self.logger = logging.getLogger("mainModule.AmazoneCloudS3Bucket.Check.module")

        '''
        results_list 返回给CSV的列表
        '''
        self.results_list = []

    def CheckBucketListObject(self):
        try:
            getObjectList = self.s3_resource.Bucket(self.getBucketName)
            for getObject in getObjectList.objects.all():
                self.logger.info(f"List Bucket Object > {getObject.key}")
                self.results_list.append("ListObject")
                break
        except Exception as e:
            '''
            这里为什么要加判断
            NoSuchBucket的报错是这样的botocore.errorfactory.NoSuchBucket
            但是不知道为什么这边调不到这个方法，所以干脆直接判断字符
            '''
            if "NoSuchBucket" in str(e):
                self.logger.info("NoSuchBucket")
                self.results_list.append("NoSuchBucket")
            else:
                self.logger.error(e)

    def CheckBucketPutObject(self):
        try:
            '''
            下面为什么要把对象的元数据设置为text/html，原因是因为默认上传文件之后，元数据为binary/octet-stream，当元数据为binary/octet-stream的时候，访问HTML文件
            会直接下载该文件，修改为text/html之后，我们访问xxxx/UzJu.html的时候，会像访问静态网站一样访问这个对象
            '''
            self.s3_resource.Object(self.getBucketName, "UzJu.html").put(
                Body="Put By https://github.com/UzJu/Cloud-Bucket-Leak-Detection-Tools.git",
                ContentType='text/html')
            self.logger.info(f"Put File Success > {self.getBucketDomain}/UzJu.html")
            self.results_list.append("PutObject")
        except Exception as e:
            self.logger.error(e)

    def CheckBucketAcl(self):
        try:
            response = self.s3.get_bucket_acl(Bucket=self.getBucketName)
            self.logger.info(f"Get Bucket Acl Success > {response}")
            self.results_list.append("GetBucketAcl")
        except Exception as e:
            self.logger.error(repr(e))

    def CheckNoSuchBucket(self):
        '''
        这里主要是用来确认，如果上面的那些方法报错了，显示NoSuchBucket的话，就证明该存储桶是可以接管的
        但是这里不会自动取创建一个存储桶去接管，而只是提示可以接管
        '''
        try:
            pass
        except Exception as e:
            self.logger.error(repr(e))

    def CheckResult(self):
        return self.results_list

    def test(self):
        pass


def CheckBucket(BucketName, BucketDomain):
    '''
    BucketName: 取下标后的存储桶名
    BucketDomain: 完整的存储桶地址
    '''
    run = AwsCloudS3Check(BucketName, BucketDomain)
    run.CheckBucketListObject()
    run.CheckBucketPutObject()
    run.CheckBucketAcl()
    if not run.CheckResult():
        pass
    else:
        conf.save_results(BucketDomain, run.CheckResult())
    module_logger.info(">" * 80)