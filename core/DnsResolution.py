#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/3/7 上午11:38
# @File    : DnsResolution.py


import dns.resolver
import logging

module_logger = logging.getLogger("mainModule.Dns")


def GetDomainDnsResolution(domain):
    try:
        cname = dns.resolver.resolve(domain, 'CNAME')
        for i in cname.response.answer:
            for j in i.items:
                return j.to_text()
    except Exception as e:
            return False

