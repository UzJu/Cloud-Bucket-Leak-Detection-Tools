#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/7/2 14:22
# @File    : conf.py

import datetime
from colorama import init, Fore, Back, Style

NowTime = datetime.datetime.now().strftime('%Y-%m-%d')

# aliyun
aliyun_id = ""
aliyun_key = ""
# aws
AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""

# tencent
tencent_cam_id = ""
tencent_cam_key = ""

# huawei
huawei_access_key_id = ""
huawei_access_key_key = ""

version = "v.0.4.0"
author = "UzJu"
email = "UzJuer@163.com"
github = "GitHub.com/UzJu"
banner = f"""
{Fore.CYAN}______            _        _   _____                 
{Fore.YELLOW}| ___ \          | |      | | /  ___|                
{Fore.GREEN}| |_/ /_   _  ___| | _____| |_\ `--.  ___ __ _ _ __  
{Fore.GREEN}| ___ \ | | |/ __| |/ / _ \ __|`--. \/ __/ _` | '_ \ 
{Fore.BLUE}| |_/ / |_| | (__|   <  __/ |_/\__/ / (_| (_| | | | |
{Fore.MAGENTA}\____/ \__,_|\___|_|\_\___|\__\____/ \___\__,_|_| |_|
         {Fore.RED} Author:{author}  Version:{version}
"""
