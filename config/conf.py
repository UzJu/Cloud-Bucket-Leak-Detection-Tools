#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/2/28 5:18 PM
# @File    : conf.py

from fake_useragent import UserAgent
UA = UserAgent(use_cache_server=False)

headers = {
    "UserAgent": UA.random
}

AK = ""
SECRET = ""
