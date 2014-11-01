#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-10-18 20:21:15
# Filename        : core/data.py
# Description     : 
from urlparse import urlparse
from xmlrpclib import ServerProxy

def get_port(url):
    name = urlparse(url)[1]
    parts = name.split(':')
    return int(parts[-1])

def get_host(url):
    name = urlparse(url)[1]
    parts = name.split(':')
    return parts[0]

    

def get_remote_info(result, ):
    if isinstance(result, dict):
        url, query = result.items()[0]
        s = ServerProxy(url)
        s.ip_query(query)
        
        secret = s.get_secret()
        return secret, get_host(url)

    if isinstance(result, str) or isinstance(result, unicode):
        return None, None

    while isinstance(result, list) or isinstance(result, tuple):
        secret, url, result = result

    return secret, get_host(url)

def parse_line(line):
    cmd, secret, line = (line.split(' ', 2) + ['', ''])[:3]
    return cmd.strip(), secret.strip(), line.strip()

