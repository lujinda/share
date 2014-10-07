#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-10-07 11:55:21
# Filename        : core/tran_server.py
# Description     : 
import socket
from core.data import parse_line
from os.path import join
from core.config import config

from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler

class Session(StreamRequestHandler):
    def handle(self):
        line = self.request.recv(1024)
        cmd, secret, line = parse_line(line)
        if secret != self.server.secret:
            self.finish()
        else:
            func = getattr(self, 'do_' + cmd, None)
            try:
                func(line)
            except:
                self.finish()



    def do_read(self, line):
        fd = open(join(self.server.dirname, line),
                'rb')
        while True:
            t_data = fd.read(self.server.block_size)
            if not t_data:
                break
            self.request.sendall(t_data)

class Server(ThreadingMixIn, TCPServer):
    allow_reuse_address = True
    def __init__(self, server_address, RequestHandlerClass,
            secret, dirname):
        TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.secret = secret
        self.dirname = dirname
        self.block_size = int(config().get('global',
                'block_size'))

class TranServer():
    def __init__(self, secret, dirname):
        port = int(config().get('global', 'listen_port'))
        self.s = Server(('', port), Session, secret, dirname)
    def _start(self):
        self.s.serve_forever()


