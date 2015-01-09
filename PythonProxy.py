# -*- coding: cp1252 -*-

import socket, thread, select
import re
import sys
import httplib


__version__ = '0.1.0 Draft 1'
BUFLEN = 8192
VERSION = 'Python Proxy/'+__version__
HTTPVER = 'HTTP/1.1'


class ConnectionHandler:
    def __init__(self, connection, address, timeout, reg, a):
        print "init %i"%a
        self.client = connection
        self.client_buffer = ''
        self.timeout = timeout
        self.reg=reg
        self.a=a
        self.data=''
        self.rclient_buffer = ''
        self.rdata = ''
        self.i=0
        while self.i<5:
            print '%i==%i start'%(self.a, self.i)
            a = self.get_base_header()
            #print a
            self.method, self.path, self.protocol = a
            print self.method, self.path, self.protocol, self.i
            if self.method=='CONNECT':
                self.method_CONNECT()
            elif self.method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT',
                    'DELETE', 'TRACE'):
                self.method_others()
            print '%i==%i end'%(self.a, self.i)
            self.i+=1
            self.target.close()
            self.client_buffer = ''
            self.data = ''
            self.rclient_buffer = ''
            self.rdata = ''
            print '%i==%i ended'%(self.a, self.i)
        self.client.close()
        #self.target.close()
        print '%i colse'%self.a
        thread.exit_thread()


    def get_base_header(self):
        #receive 
        while 1:
            self.data = self.client.recv(BUFLEN)
            self.client_buffer += self.data
            if len(self.data)!=BUFLEN:
                break
            print '%i==>%s<==\n'%(self.i, self.client_buffer)
        end = self.client_buffer.find('\n')
        data = (self.client_buffer[:end+1]).split()
        if len(data)<3 :
            thread.exit_thread()
        print '===', data, '===', data[0], '===', data[1], '===', data[2], '===' 
        self.client_buffer = self.client_buffer[end+1:]
        return data


    def method_CONNECT(self):
        self._connect_target(self.path)
        self.client.send(HTTPVER+' 200 Connection established\n'+
                'Proxy-agent: %s\n\n'%VERSION)
        self.client_buffer = ''
        self._read_write()        


    def method_others(self):
        self.path = self.path[7:]
        i = self.path.find('/')
        host = self.path[:i]        
        path = self.path[i:]
        self.host = host
        self.hpath = path
        if host=='debug.net':
            self.debug()

        elif self.reg.match(self.path):
            print '%iDebuging == %s'%(self.a,self.path)
            req = '%s %s %s\n'%(self.method, path, self.protocol)+self.client_buffer
            #print 'request is ==>\n%s'%req
            self._connect_target(host)
            self.target.send(req)
            self.client_buffer = ''
            self._read_write_debug()

        else:
            self._connect_target(host)
            self.target.send('%s %s %s\n'%(self.method, path, self.protocol)+self.client_buffer)
            self.client_buffer = ''
            self._read_write()





    def debug(self):
        self.client.send("HTTP/1.1 200 OK\r\n\r\nHello World!\r\n\r\n")


class Handler:
    def __init__(self, connection, address, timeout, reg, a):
        print "init %i"%a
        self.client = connection
        self.client_buffer = ''
        self.timeout = timeout
        self.reg=reg
        self.a=a
        self.data=''
        self.rclient_buffer = ''
        self.rdata = ''
        self.i=0
        while self.i<5:
            print '%i==%i start'%(self.a, self.i)
            while 1:
                data = self.client.recv(BUFLEN)
                self.client_buffer += data
                print data
                if len(data)!=BUFLEN:
                    break
            self.proxy_it()
            self.client_buffer = ''
            self.server_buffer = ''

    def proxy_it(self):
        end = self.client_buffer.find('\n')
        data = (self.client_buffer[:end+1]).split()
        print data
        if len(data)<3 :
            thread.exit_thread()
        self.client_buffer = self.client_buffer[end+1:]
        self.method, self.path, self.protocol = data
        if self.path == "" :
            #debug_url
            return
        elif self.reg.match(self.path):
            #debug_it()
            return
        self.path = self.path[7:]
        print self.path
        i = self.path.find('/')
        host = self.path[:i]        
        self.path = self.path[i:]
        if self.method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT',
                'DELETE', 'TRACE'):
            self.do_proxy(host)
            self.client.send(self.server_buffer)


    def do_proxy(self,host):
        i = host.find(':')
        if i == -1 :
            port = 80
        else :
            port = host[i+1:]
            host = host[:i]
            port = int(port)
        host = socket.gethostbyname(host)
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
