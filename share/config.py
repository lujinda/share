#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-11-01 14:57:47
# Filename        : share/config.py
# Description     : 
import ConfigParser, os

cfg_file = ['share.cfg', '/etc/share.cfg']

def config():
    cfg = ConfigParser.ConfigParser()
    for f in cfg_file:
        if os.path.exists(f):
            cfg.read(f)
            return cfg

    raise Exception('share.cfg does not exist')
    
