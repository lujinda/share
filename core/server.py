#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-10-07 10:58:23
# Filename        : core/server.py
# Description     : from xmlrpclib import ServerProxy, Fault
from os.path import join, abspath, isfile, basename
from urlparse import urlparse
from core.config import config
import sys
import os
from xmlrpclib import ServerProxy, Fault, Binary
from core.data import get_port, get_remote_info
from core.sock import open_file
from SocketServer import ThreadingMixIn
from SimpleXMLRPCServer import SimpleXMLRPCServer

SimpleXMLRPCServer.allow_reuse_address = True
UNHANDLED = 100
ACCESS_DENIED = 200
MAX_HISTORY_LEGTH = 100

class ThreadRPC(ThreadingMixIn, SimpleXMLRPCServer): # 并发xml-rpc,默认情况下SimpleXMLRPCServer是单线程的,在本项目中会阻塞
    pass

class UnhandledQuery(Fault):
    def __init__(self, message = "Couldn't handle the query"):
        Fault.__init__(self, UNHANDLED, message)

class AccessDenied(Fault):
    def __init__(self, message = "Access denied"):
        Fault.__init__(self, ACCESS_DENIED, message)


def inside(dirname, name):
    dirname = abspath(dirname)
    name = abspath(name)
    return name.startswith(join(dirname, ''))


class Node():
    def __init__(self, url , dirname, secret):  # 以url来区分节点
        cfg = config()
        self.url = url 
        self.file_temp_list = {}
        self.dirname = dirname
        self.secret = secret
        self.block_size = int(cfg.get('global', 
            'block_size')) 
        self.listen_port = int(cfg.get('global',
            'listen_port'))
        self.known = set() # 存放的是节点信息


    def query(self, query, history = []):
        try:
            return self._handle(query)
        except UnhandledQuery: # 如果自己没有这文件，则去其他节点上找
            history = history + [self.secret]  # 本来是以url来判断是否会循环远程调用，假如a,b两台机器，同时开启，对于自己而言url都是localhost，在遍历节点时，会循环，会阻塞，死锁。因为a中的self.known中有b,b中也有a。 a调用b,b调用a....最终阻塞
            if len(history) > MAX_HISTORY_LEGTH:raise
            return self._broadcast(query, history)

    def _handle(self, query):
        name = join(self.dirname, query)
        if not isfile(name):raise UnhandledQuery
        if not inside(self.dirname, name):raise AccessDenied
        return name # 如果在本地，则返回名字

    def get_secret(self):
        return self.secret

    def open_file(self, query):
        result = self.query(query)
        secret, host = get_remote_info(result) # 如果是本地会返回None,否则是一个url，根据它来下载
        if not host:
            return 0
        fd = open_file(secret, query, host, self.listen_port)
        return fd



    def fetch(self, query, secret):
        if secret != self.secret:raise
        fd = self.open_file(query) # 打通与远程文件的数据传输通道
        

        if not fd : # 如果在本地，就不需要再执行下面的了
            return 0

        with open(join(self.dirname, query), 'wb') as to_fd:
            while True:
                data  = fd.read(self.block_size)
                if not data:break
                to_fd.write(data)
                #sys.stdout.write(data)
            
        fd.close()
        return 0

    def cat(self, query, read_size):
        fd = self.open_file(query) or \
                open(join(self.dirname, query), 'rb')

        if isinstance(read_size, int) and read_size >0: 
            self.__cat(fd, read_size)

        fd.close()

        return 0

    def __cat(self, fd, read_size):
        for i in xrange(read_size):
            data = fd.read(1)
            if not data:
                break
            sys.stdout.write(data)
        sys.stdout.write('\n')
        sys.stdout.flush()

    # handle_read 方法已over
    def handle_read(self, query, secret):
        name = join(self.dirname, query)
        file_id = secret + name
        if file_id not in self.file_temp_list:
            self.file_temp_list[file_id] = open(name, 'rb')

        data = self.file_temp_list[file_id].read(self.block_size)
        if not data:
            del self.file_temp_list[file_id]
            return None

        return Binary(data)
        #return Binary(open(name, 'rb').read())

    def ls_dir(self,path='.'):
        dir_tree = []
        os.chdir(self.dirname)
        for root, dirs, files in os.walk("."):
            root = basename(root)
            for f in files:
                dir_tree.append(join(root, f))
        os.chdir('..')

        return dir_tree

    def ls(self, path = '.'):
        request = {}
        request[self.url] = self.ls_dir()
        for other in self.known.copy():
            try:
                s = ServerProxy(other)
                request[other] = s.ls_dir()
            except Exception:
                pass
        return request

    def _broadcast(self, query, history):
        for other in self.known.copy():
            try:
                s = ServerProxy(other, allow_none = True)
                secret = s.get_secret()
                if secret in history:continue # 如果secret已经在历史记录中了，就不要再query，这样会成一个死循环,理由见query方法
                return secret, other, s.query(query, history)
            except Fault, f:
                if f.faultCode == UNHANDLED:pass
                else:self.known.remove(other) # 如果不是因为没找到，而是其他原因的异常，则把这个节点删除
            except Exception,e:
                self.known.remove(other) # 同上

        raise UnhandledQuery

    def hello(self, other, secret):
        if secret != self.secret:raise
        self.known.add(other) 
        return 0

    def _start(self):

        self.s = ThreadRPC(("", get_port(self.url)), 
                logRequests = False, allow_none = True)
        self.s.register_instance(self)
        self.s.serve_forever()

