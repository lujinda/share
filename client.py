#!/usr/bin/env python
#coding:utf8
# Author          : tuxpy
# Email           : q8886888@qq.com
# Last modified   : 2014-10-02 14:08:54
# Filename        : client.py
# Description     : 
from xmlrpclib import ServerProxy, Fault
from cmd import Cmd
from random import choice
from string import lowercase
from core.server import Node, UNHANDLED
from core.data import get_port, get_host
from threading import Thread
from time import sleep

import sys
HEAD_START = 0.1
SECRET_LENGTH = 100


def randomString(length):
    chars = []
    for i in range(length):
        chars.append(choice(lowercase))

    return ''.join(chars)

class Client(Cmd):
    prompt = '> '
    def __init__(self, url , dirname):
        Cmd.__init__(self)
        self.url = url
        self.port = get_port(url)  # 这个要当信息广播出去
        self.secret = randomString(SECRET_LENGTH)
        node = Node(url, dirname, self.secret)
        t_node = Thread(target = node._start)
        t_node.setDaemon(True)
        t_node.start()

        sleep(HEAD_START)
        self.server = ServerProxy(url)
        t_update_known = Thread(target = self.update_known)
        t_update_known.setDaemon(True)
        t_update_known.start()
        
    def do_fetch(self, arg):
        try:
            self.server.fetch(arg, self.secret)
        except Fault, f:
            if f.faultCode != UNHANDLED:raise
            print "Couldn't find the file", arg

    def do_ls(self, path):
        for url,files in self.server.ls().items():
            print '%s\n\t%s' % (get_host(url), '\n\t'.join(files))
        
    def update_known(self):
        from core.sock import sock
        sock = sock()
        sock.broadcast(str(self.port))  # 把自己的xml-rpc端口广播给别人
        while True:
            url = sock.recv_url()
            self.server.hello(url, self.secret) # 当收到节点信息时，更新节点

    def do_exit(self, arg):
        print
        sys.exit()

    do_EOR = do_exit

def main():
    import os
    cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(cwd) #  切换成程序所在目录

    from core.config import config
    cfg = config()
    directory = cfg.get('global', 'share_dir') 
    if not os.path.isdir(directory):
        sys.stderr.write("%s not is exist\n" % directory)
        sys.exit(1)
        
    url = 'http://localhost:' + cfg.get('global', 'data_port')

    client = Client(url, directory)
    client.cmdloop()

if __name__ == "__main__":
    main()
