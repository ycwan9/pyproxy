# -*- coding: cp1252 -*-

import socket, thread, select
import re
import sys
import httplib
import SocketServer

__version__ = '0.1.0 Draft 1'
BUFLEN = 8192
VERSION = 'Python Proxy/'+__version__
HTTPVER = 'HTTP/1.1'

class socketHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        i = 0
        while i < 5 :
            first_line = self.rfile.readline()
            first_line_s = first_line.split()
            if len(first_line_s)<3 :
                print 'first line error : %s'%first_line
            method, rurl, version = first_line_s
            if method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE'):
                do_proxy(method, rurl, version, self.rfile, self.wfile)
                i+=1




def do_proxy(method, rurl, version, rfile, wfile):
    rurl = rurl[7:]
    i = rurl.find('/')
    host = rurl[:i]
    path = rurl[i:]
    i = host.find(':')
    if i == -1 :
        port = 80
    else :
        port = host[i+1:]
        host = host[:i]
        port = int(port)
    #receive others
    #
    #
    #
    #
    #
    #
    #
    #
    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ser.connect((host,port))
    ser.send("%s %s %s\r\n"%(self.method,self.path,self.protocol)+self.client_buffer)
    while 1:
        data = ser.recv(BUFLEN)
        self.server_buffer += data
        if len(data)!=BUFLEN:
            break




 
 





def start_server(host='localhost', port=8080, IPv6=False, timeout=60,
                  handler=Handler):
    if IPv6==True:
        soc_type=socket.AF_INET6
    else:
        soc_type=socket.AF_INET
    reg = 'asdcfasdvasdv'
    #reg = '.*'
    #if len(sys.argv)>1:
    #    reg = '.*%s.*'%sys.argv[1]
    regExp = re.compile(reg)
    soc = socket.socket(soc_type)
    soc.bind((host, port))
    print "Serving on %s:%d."%(host, port)#debug
    soc.listen(0)
    a=0
    while 1:
        thread.start_new_thread(handler, soc.accept()+(timeout,regExp,a))
        a+=1


if __name__ == '__main__':
    start_server()
