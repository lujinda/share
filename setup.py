#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-11-01 15:19:11
# Filename        : setup.py
# Description     : 
from distutils.core import setup
import os

setup(
    name = 'share',
    version = '1.0.4',
    author = 'tuxpy',
    author_email = 'q8886888@qq.com',
    license = 'GPL3',
    description = 'shared files in lan',
    url = 'https://github.com/lujinda/share',
    packages = [
        'share', # 包含的包，本项目，就是当前目录下的share
        ],
    scripts = ['bin/share'], # 安装后的，可执行文件
    data_files = [('/etc', ['share.cfg'])], # 在本项目中，就是配置文件share.cfg复制到/etc，如有man文件，也可以复制过去
        )

