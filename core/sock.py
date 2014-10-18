#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-10-17 14:49:02
# Filename        : core/sock.py
# Description     : 
import socket
from core.config import config
import sys

class open_file:
    def __init__(self, secret, query, host, listen_port):
        self.secret = secret
        self.query = query
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__s.connect((host, listen_port))
        self.__s.sendall("read %s %s\n" %  
                (self.secret, self.query))
        

    def read(self, block_size = 1024):
        return self.__s.recv(block_size)

    def close(self):
        self.__s.close()

class sock:
    def __init__(self):

        cfg= config()
        self.listen_port = int(cfg.get('global', 
            'listen_port'))
        self.__re = self.__recv() # 用来接收数据包
        self.me_url = None # 记录自己的ip，暂时弃用

    def __made_broad_sock(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        return s

    def broadcast(self, port):
        self.port = port # 要发送的内容，端口号str
        s_broad = self.__made_broad_sock()
        s_broad.bind(('', 0))
        s_broad.sendto(self.port, ("172.17.255.255", 
            self.listen_port))

        s_broad.close()


    def __recv(self):
        s_recv = self.__made_broad_sock()
        s_recv.bind(('', self.listen_port))
        while True:
            port, address = s_recv.recvfrom(1024)
            if port.strip().isdigit():  # 广播发的信息中，端口就是端口
                yield (address[0], port)
                s_recv.sendto(':'.join([address[0], self.port]), # 当收到的是广播包时，需要给对方一个回复
                    (address[0], self.listen_port))
            else:  # 如果收到的不是广播包的话，就记录对方的信息，并不要发回复包了，要不然就死循环了
                self.me_url, port = port.split(':') 
                yield (address[0], port)

    def recv_url(self):
        ip_port = self.__re.next()
        return 'http://' + ":".join(ip_port)
