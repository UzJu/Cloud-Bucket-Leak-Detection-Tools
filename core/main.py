#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/7/2 14:22
# @File    : main.py

from config.logs import logger
from plugins.results import aliyun_save_file
from core import aliyunOss
from core import aws
import urllib.parse
import prettytable as pt
import multiprocessing


def aliyun_file_scan(filename):
    target_file = open(filename, mode='r', encoding='utf-8')
    p = multiprocessing.Pool(processes=3)
    for i in target_file.read().splitlines():
        p.apply_async(aliyun, args=(i,))
    p.close()
    p.join()
    p.terminate()


def aliyun(target):
    """

    :desc: aliyun Bucket Scan function
    :param target: Bucket URL
    :return:
    """
    logger.log("INFOR", f"开始扫描> {target}")
    aliyun_print_table_header = pt.PrettyTable(
        ['Bucket', 'BucketHijack', 'GetBucketObjectList', 'PutBucketObject', 'GetBucketAcl', 'PutBucketAcl',
         'GetBucketPolicy'])
    aliyun_scan_results = {}
    get_domain = urllib.parse.urlparse(target).netloc
    if get_domain == "":
        get_target_list = target.split('.')
        aliyunOss_Check_init = aliyunOss.Aliyun_Oss_Bucket_Check(target=get_target_list[0],
                                                                 location=get_target_list[1])
        aliyunOss_Exploit_init = aliyunOss.Aliyun_Oss_Bucket_Exploit(target=get_target_list[0],
                                                                     location=get_target_list[1])
        if aliyunOss_Check_init.Aliyun_Oss_BucketDoesBucketExist():
            logger.log("INFOR", f"{target}> 当前存储桶不存在, 尝试劫持存储桶")
            if aliyunOss_Exploit_init.Aliyun_Oss_CreateBucket_Exp():
                logger.log("ALERT", f"{target}> 新创建/新版存储桶不可劫持")
            else:
                aliyunOss_Exploit_init.Aliyun_Oss_PutObject_Exp()
                aliyunOss_Exploit_init.Aliyun_Oss_PutBucketPolicy_Exp()
                aliyunOss_Exploit_init.Aliyun_Oss_GetBucketPolicy_Exp()
                aliyunOss_Exploit_init.Aliyun_Oss_PutBucketAcl_Exp()
                aliyun_scan_results.update({"BucketDoesBucketExist": "true"})
        else:
            aliyun_scan_results.update({"BucketDoesBucketExist": "false"})
            if aliyunOss_Check_init.Aliyun_Oss_GetBucketObject_List():
                logger.log("INFOR", f"{target}> 存储桶对象可遍历")
                aliyun_scan_results.update({"GetBucketObject": "true"})
            else:
                logger.log("ALERT", f"{target}> 存储桶对象不可遍历")
                aliyun_scan_results.update({"GetBucketObject": "false"})

            if aliyunOss_Check_init.Aliyun_Oss_PutBucketObject():
                logger.log("INFOR", f"{target}> 可未授权上传对象至存储桶（可导致覆盖已有对象）")
                aliyun_scan_results.update({"PutBucketObject": "true"})
            else:
                logger.log("ALERT", f"{target}> 不可未授权上传对象至存储桶")
                aliyun_scan_results.update({"PutBucketObject": "false"})

            if aliyunOss_Check_init.Aliyun_Oss_GetBucketAcl():
                logger.log("INFOR", f"{target}> 可公开访问存储桶ACL策略")
                aliyun_scan_results.update({"GetBucketAcl": "true"})
            else:
                logger.log("ALERT", f"{target}> 不可公开访问存储桶ACL策略")
                aliyun_scan_results.update({"GetBucketAcl": "false"})

            if aliyunOss_Check_init.Aliyun_Oss_PutBucketAcl():
                logger.log("INFOR", f"{target}> 可上传覆盖存储桶ACL策略")
                aliyun_scan_results.update({"PutBucketAcl": "true"})
            else:
                logger.log("ALERT", f"{target}> 不可上传覆盖存储桶ACL策略")
                aliyun_scan_results.update({"PutBucketAcl": "false"})

            results_policy = aliyunOss_Check_init.Aliyun_Oss_GetBucketPolicy()
            if results_policy:
                logger.log("INFOR", f"{target}> 可公开获取存储桶Policy策略组")
                logger.log("INFOR", f"{target}Policy> {results_policy}")
                aliyun_scan_results.update({"GetBucketPolicy": "true"})
            else:
                logger.log("ALERT", f"{target}> 不可公开获取存储桶Policy策略")
                aliyun_scan_results.update({"GetBucketPolicy": "false"})

            aliyun_print_table_header.add_row([target,
                                               aliyun_scan_results['BucketDoesBucketExist'],
                                               aliyun_scan_results['GetBucketObject'],
                                               aliyun_scan_results['PutBucketObject'],
                                               aliyun_scan_results['GetBucketAcl'],
                                               aliyun_scan_results['PutBucketAcl'],
                                               aliyun_scan_results['GetBucketPolicy']])
            aliyun_save_file(target,
                             aliyun_scan_results['BucketDoesBucketExist'],
                             aliyun_scan_results['GetBucketObject'],
                             aliyun_scan_results['PutBucketObject'],
                             aliyun_scan_results['GetBucketAcl'],
                             aliyun_scan_results['PutBucketAcl'],
                             aliyun_scan_results['GetBucketPolicy'])
            print(aliyun_print_table_header, "\n")
    else:
        aliyun(get_domain)


def AmazoneS3(target):
    """

    :desc: aws bucket scan
    :param target: bucket url
    :return:
    """
    get_domain = urllib.parse.urlparse(target).netloc
    if get_domain == "":
        logger.log("INFOR", f"开始扫描> {target}")
        get_target_list = target.split(".")
        aws_check_init = aws.Amazone_Cloud_S3Bucket_Check(target=get_target_list[0],
                                                          location=get_target_list[1])
        if aws_check_init.Check_Bucket_ListObject():
            logger.log("INFOR", f"{target}> 存储桶对象可遍历")
        else:
            logger.log("ALERT", f"{target}> 存储桶对象不可遍历")

        if aws_check_init.Check_Bucket_PutObject():
            logger.log("INFOR", f"{target}> 可未授权上传对象至存储桶（可覆盖存储桶已有对象）")
        else:
            logger.log("ALERT", f"{target}> 不可未授权上传对象至存储桶（可覆盖存储桶已有对象）")

        if aws_check_init.Check_Bucket_GetBucketAcl():
            logger.log("INFOR", f"{target}> 存储桶ACL策略可公开获取")
        else:
            logger.log("ALERT", f"{target}> 存储桶ACL策略不可公开")
    else:
        AmazoneS3(get_domain)
