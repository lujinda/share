#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-10-03 13:57:31
# Filename        : /data/github/share/core/data.py
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

def get_remote_url(result):
    if isinstance(result, str):
        return None

    while isinstance(result, list) or isinstance(result, tuple):
        url, result = result

    return url

