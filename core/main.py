#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/7/2 14:22
# @File    : main.py

from config.logs import logger
from plugins.results import *
import urllib.parse
import prettytable as pt
import multiprocessing

from core.aliyun import oss
from core.aws import aws
from core.tencent import cos
from core.huaweiyun import obs


def Aliyun_file_scan(filename):
    target_file = open(filename, mode='r', encoding='utf-8')
    p = multiprocessing.Pool(processes=3)
    for i in target_file.read().splitlines():
        p.apply_async(Aliyun_OSS, args=(i,))
    p.close()
    p.join()
    p.terminate()


def Aliyun_OSS(target):
    """

    :desc: aliyun Bucket Scan function
    :param target: Bucket URL
    :return:
    """
    logger.log("INFOR", f"开始扫描> {target}")
    aliyun_print_table_header = pt.PrettyTable(
        ['Bucket', 'BucketHijack', 'GetBucketObjectList', 'PutBucketObject', 'GetBucketAcl', 'PutBucketAcl',
         'GetBucketPolicy'])
    aliyun_scan_results = {
        "BucketName": target,
        "BucketDoesBucketExist": False,
        "BucketHijack": False,
        "GetBucketObjectList": False,
        "PutBucketObject": False,
        "GetBucketAcl": False,
        "PutBucketAcl": False,
        "GetBucketPolicy": False,
    }
    get_domain = urllib.parse.urlparse(target).netloc
    if get_domain == "":
        get_target_list = target.split('.')
        aliyunOss_Check_init = oss.Aliyun_Oss_Bucket_Check(target=get_target_list[0],
                                                           location=get_target_list[1])
        aliyunOss_Exploit_init = oss.Aliyun_Oss_Bucket_Exploit(target=get_target_list[0],
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
        else:
            if aliyunOss_Check_init.Aliyun_Oss_GetBucketObject_List():
                logger.log("INFOR", f"{target}> 存储桶对象可遍历")
                aliyun_scan_results['GetBucketObjectList'] = True
            else:
                logger.log("ALERT", f"{target}> 存储桶对象不可遍历")

            if aliyunOss_Check_init.Aliyun_Oss_PutBucketObject():
                logger.log("INFOR", f"{target}> 可未授权上传对象至存储桶（可导致覆盖已有对象）")
                aliyun_scan_results['PutBucketObject'] = True
            else:
                logger.log("ALERT", f"{target}> 不可未授权上传对象至存储桶")

            if aliyunOss_Check_init.Aliyun_Oss_GetBucketAcl():
                logger.log("INFOR", f"{target}> 可公开访问存储桶ACL策略")
                aliyun_scan_results['GetBucketAcl'] = True
            else:
                logger.log("ALERT", f"{target}> 不可公开访问存储桶ACL策略")

            if aliyunOss_Check_init.Aliyun_Oss_PutBucketAcl():
                logger.log("INFOR", f"{target}> 可上传覆盖存储桶ACL策略")
                aliyun_scan_results['PutBucketAcl'] = True
            else:
                logger.log("ALERT", f"{target}> 不可上传覆盖存储桶ACL策略")

            results_policy = aliyunOss_Check_init.Aliyun_Oss_GetBucketPolicy()
            if results_policy:
                logger.log("INFOR", f"{target}> 可公开获取存储桶Policy策略组")
                logger.log("INFOR", f"{target}Policy> {results_policy}")
                aliyun_scan_results['GetBucketPolicy'] = True
            else:
                logger.log("ALERT", f"{target}> 不可公开获取存储桶Policy策略")

            aliyun_print_table_header.add_row([target,
                                               aliyun_scan_results['BucketDoesBucketExist'],
                                               aliyun_scan_results['GetBucketObjectList'],
                                               aliyun_scan_results['PutBucketObject'],
                                               aliyun_scan_results['GetBucketAcl'],
                                               aliyun_scan_results['PutBucketAcl'],
                                               aliyun_scan_results['GetBucketPolicy']])
            aliyun_save_file(target,
                             aliyun_scan_results['BucketDoesBucketExist'],
                             aliyun_scan_results['GetBucketObjectList'],
                             aliyun_scan_results['PutBucketObject'],
                             aliyun_scan_results['GetBucketAcl'],
                             aliyun_scan_results['PutBucketAcl'],
                             aliyun_scan_results['GetBucketPolicy'])
            print(aliyun_print_table_header)
    else:
        Aliyun_OSS(get_domain)


def Tencent_Cloud_Cos(target):
    tencent_cloud_print_table_header = pt.PrettyTable(
        ['Bucket', 'ListObject', 'PutObject', 'GetBucketACL'])
    tencent_cloud_results = {
        "BucketName": target,
        "ListObject": False,
        "PutObject": False,
        "GetBucketACL": False
    }
    get_domain = urllib.parse.urlparse(target).netloc
    if get_domain == "":
        if "cos" not in target:
            logger.log("ALERT", f"当前{target}非COS存储桶地址")
            return
        logger.log("INFOR", f"开始扫描> {target}")
        get_target_list = target.split(".")
        tencent_check_init = cos.TenCent_Cloud_OBS_Check(target=get_target_list[0],
                                                         location=get_target_list[2])
        if tencent_check_init.ListObject():
            tencent_cloud_results['ListObject'] = True
        if tencent_check_init.PutObject():
            tencent_cloud_results['PutObject'] = True
        if tencent_check_init.GetBucketACL():
            tencent_cloud_results['GetBucketACL'] = True
    else:
        Tencent_Cloud_Cos(target)
    tencent_cloud_print_table_header.add_row([target,
                                              tencent_cloud_results['ListObject'],
                                              tencent_cloud_results['PutObject'],
                                              tencent_cloud_results['GetBucketACL']])
    tencent_save_file(target,
                      tencent_cloud_results['ListObject'],
                      tencent_cloud_results['PutObject'],
                      tencent_cloud_results['GetBucketACL'])
    print(tencent_cloud_print_table_header)


def Huawei_Cloud_OBS(target):
    huawei_cloud_print_table_header = pt.PrettyTable(
        ['Bucket', 'ListObject', 'PutObject', 'GetBucketACL'])
    huawei_cloud_results = {
        "BucketName": target,
        "ListObject": False,
        "PutObject": False,
        "GetBucketACL": False
    }
    get_domain = urllib.parse.urlparse(target).netloc
    if get_domain == "":
        if "obs" not in target:
            logger.log("ALERT", f"当前{target}非OBS存储桶地址")
            return
        logger.log("INFOR", f"开始扫描> {target}")
        get_target_list = target.split(".")
        huaweiyun_check_init = obs.HuaWeiCloud_OBS_Check(target=get_target_list[0],
                                                         location=get_target_list[2])
        if huaweiyun_check_init.ListObject():
            huawei_cloud_results['ListObject'] = True
        if huaweiyun_check_init.PutObject():
            huawei_cloud_results['PutObject'] = True
        if huaweiyun_check_init.GetBucketACL():
            huawei_cloud_results['GetBucketACL'] = True
    else:
        Huawei_Cloud_OBS(target)
    huawei_cloud_print_table_header.add_row([target,
                                             huawei_cloud_results['ListObject'],
                                             huawei_cloud_results['PutObject'],
                                             huawei_cloud_results['GetBucketACL']])
    huawei_save_file(target,
                     huawei_cloud_results['ListObject'],
                     huawei_cloud_results['PutObject'],
                     huawei_cloud_results['GetBucketACL'])
    print(huawei_cloud_print_table_header)


def AmazoneS3(target):
    """

    :desc: aws bucket scan
    :param target: bucket url
    :return:
    """
    aws_print_table_header = pt.PrettyTable(
        ['Bucket', 'ListObject', 'PutObject', 'GetBucketACL'])
    aws_results = {
        "BucketName": target,
        "ListObject": False,
        "PutObject": False,
        "GetBucketACL": False
    }
    get_domain = urllib.parse.urlparse(target).netloc
    if get_domain == "":
        logger.log("INFOR", f"开始扫描> {target}")
        get_target_list = target.split(".")
        aws_check_init = aws.Amazone_Cloud_S3Bucket_Check(target=get_target_list[0],
                                                          location=get_target_list[1])
        if aws_check_init.Check_Bucket_ListObject():
            logger.log("INFOR", f"{target}> 存储桶对象可遍历")
            aws_results['ListObject'] = True
        else:
            logger.log("ALERT", f"{target}> 存储桶对象不可遍历")

        if aws_check_init.Check_Bucket_PutObject():
            logger.log("INFOR", f"{target}> 可未授权上传对象至存储桶（可覆盖存储桶已有对象）")
            aws_results['PutObject'] = True
        else:
            logger.log("ALERT", f"{target}> 不可未授权上传对象至存储桶（可覆盖存储桶已有对象）")

        if aws_check_init.Check_Bucket_GetBucketAcl():
            logger.log("INFOR", f"{target}> 存储桶ACL策略可公开获取")
            aws_results['GetBucketACL'] = True
        else:
            logger.log("ALERT", f"{target}> 存储桶ACL策略不可公开")
    else:
        AmazoneS3(get_domain)
    aws_print_table_header.add_row([target,
                                    aws_results['ListObject'],
                                    aws_results['PutObject'],
                                    aws_results['GetBucketACL']])
    aws_save_file(target,
                  aws_results['ListObject'],
                  aws_results['PutObject'],
                  aws_results['GetBucketACL'])
    print(aws_print_table_header)
