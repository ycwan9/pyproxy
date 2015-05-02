# -*- coding: utf-8 -*-
import httpServer, select, socket, SocketServer, urlparse, httplib
import proxy
import debug_server

    #__base = BaseHTTPServer.BaseHTTPRequestHandler
    #__base_handle = __base.handle

class ProxyHandler (httpServer.pyProxyHTTPRequestHandler):
    server_version = "PyProxy/0.1"
    rbufsize = 0                        # self.rfile Be unbuffered

    def do_CONNECT(self):
        netloc = self.path
        i = netloc.find(':')
        if i >= 0:
            self.host_and_port = netloc[:i], int(netloc[i+1:])
        else:
            self.host_and_port = netloc, 80
        try:
            print "\t" "connect to %s:%d" %self.host_and_port
            self.log_request(200)
            self.do_ssl_rw()
        finally:
            print "\t" "bye"
            self.connection.close()

    def do_GET(self):
        #you can use url like
        #http://localhost:8080/http:google.com/
        #to debug it
        debug = 0
        #if (len(self.path)>5) and (self.path[:5] == "/http"):
        #    self.path = self.path[1:]
        self.ppath = urlparse.urlparse(self.path, 'http')
        #generate request path
        self.rpath = urlparse.urlunparse(("", "", self.ppath.path, self.ppath.params, self.ppath.query, self.ppath.fragment))
        if self.ppath.scheme != 'http' or self.ppath.fragment or not self.ppath.netloc:
            self.send_error(400, "bad url %s" % self.path)
            return
        if debug:
            del self.headers["Host"]
            self.headers.headers.append("Host:%s"%netloc)
        #set port
        if self.ppath.port:
            rport = int(self.ppath.port)
        else:
            rport = 80
        self.host_and_port = (self.ppath.hostname, rport)
        #soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #try:
        self.log_request()
        #modify headers
        del self.headers['Connection']
        del self.headers['Proxy-Connection']
        self.headers.headers.append('Connection:close\r\n')
        header = ''.join(self.headers.headers)
        #gen requset str
        self.request = '%s %s %s\r\n%s\r\n'%(self.command, self.rpath, self.request_version, header)
        #get requset data
        data = ''
        if self.headers.has_key('Content-Length'):
            i = int(self.headers.getheader('Content-Length'))
            data = self.rfile.read(i)
        self.request += data
        #do the http proxy
        self.do_http()
        #proxy.proxy((host,port), self.connection, self.send_error, request, self.req_queue)
        print "\t" "bye"
        #soc.close()
        #self.connection.close()

    #def _read_write(self, soc, max_idling=20):
    #    iw = [self.connection, soc]
    #    ow = []
    #    count = 0
    #    while 1:
    #        count += 1
    #        (ins, _, exs) = select.select(iw, ow, iw, 3)
    #        if exs: break
    #        if ins:
    #            for i in ins:
    #                if i is soc:
    #                    out = self.connection
    #                else:
    #                    out = soc
    #                data = i.recv(8192)
    #                if data:
    #                    out.send(data)
    #                    count = 0
    #        else:
    #            print "\t" "idle", count
    #        if count == max_idling: break

