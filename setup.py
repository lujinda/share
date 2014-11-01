#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-11-01 14:40:22
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
        'share',
        ],
    scripts = ['bin/share'],
    data_files = [('/etc/share', ['share.cfg'])],
        )


