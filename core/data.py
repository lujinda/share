#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-10-01 15:10:58
# Filename        : core/data.py
# Description     : 
from urlparse import urlparse

def get_port(url):
    name = urlparse(url)[1]
    parts = name.split(':')
    return int(parts[-1])

def get_host(url):
    name = urlparse(url)[1]
    parts = name.split(':')
    return parts[0]
