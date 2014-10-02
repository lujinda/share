#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-10-01 13:12:28
# Filename        : core/config.py
# Description     : 
import ConfigParser, os

cfg_file = 'share.cfg'

def config():
    cfg = ConfigParser.ConfigParser()
    if os.path.exists(cfg_file):
        cfg.read(cfg_file)
        return cfg
    else:
        return None
    
