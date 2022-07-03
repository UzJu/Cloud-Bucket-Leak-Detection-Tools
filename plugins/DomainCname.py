#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/7/2 19:59
# @File    : DomainCname.py

import dns.resolver
from config.logs import logger


def Get_Domain_Cname(domain):
    try:
        cname = dns.resolver.resolve(domain, 'CNAME')
        for i in cname.response.answer:
            for j in i.items:
                return j.to_text()
    except Exception as e:
        logger.log("ERROR", repr(e))
        return False
