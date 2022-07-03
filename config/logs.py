#!/usr/bin/python3.8.4 (python版本)
# -*- coding: utf-8 -*-
# @Author  : UzJu@菜菜狗
# @Email   : UzJuer@163.com
# @Software: PyCharm
# @Time    : 2022/7/2 14:21
# @File    : logs.py
import sys
import pathlib

from loguru import logger

# Log Code From https://github.com/shmilylty/OneForAll/
# 路径设置
relative_directory = pathlib.Path(__file__).parent.parent
result_save_dir = relative_directory.joinpath('logs')
log_path = result_save_dir.joinpath('bucket_scan.log')

# 日志配置
# 终端日志输出格式
stdout_fmt = '<cyan>{time:HH:mm:ss,SSS}</cyan> ' \
             '[<level>{level: <5}</level>] ' \
             '<blue>{module}</blue>:<cyan>{line}</cyan> - ' \
             '<level>{message}</level>'
# 日志文件记录格式
logfile_fmt = '<light-green>{time:YYYY-MM-DD HH:mm:ss,SSS}</light-green> ' \
              '[<level>{level: <5}</level>] ' \
              '<cyan>{process.name}({process.id})</cyan>:' \
              '<cyan>{thread.name: <18}({thread.id: <5})</cyan> | ' \
              '<blue>{module}</blue>.<blue>{function}</blue>:' \
              '<blue>{line}</blue> - <level>{message}</level>'

logger.remove()
logger.level(name='TRACE', color='<cyan><bold>', icon='✏️')
logger.level(name='DEBUG', color='<blue><bold>', icon='🐞 ')
logger.level(name='INFOR', no=20, color='<green><bold>', icon='ℹ️')
logger.level(name='QUITE', no=25, color='<green><bold>', icon='🤫 ')
logger.level(name='ALERT', no=30, color='<yellow><bold>', icon='⚠️')
logger.level(name='ERROR', color='<red><bold>', icon='❌️')
logger.level(name='FATAL', no=50, color='<RED><bold>', icon='☠️')

logger.add(sys.stderr, level='INFOR', format=stdout_fmt, enqueue=True)

logger.add(log_path, level='DEBUG', format=logfile_fmt, enqueue=True, encoding='utf-8')
logger.disabled = True
