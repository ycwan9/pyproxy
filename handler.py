import BaseHTTPServer, select, socket, SocketServer, urlparse, httplib
    __base = BaseHTTPServer.BaseHTTPRequestHandler
    __base_handle = __base.handle

class ProxyHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    server_version = "PyProxy/" + __version__
    rbufsize = 0                        # self.rfile Be unbuffered

    def handle(self):
        (ip, port) =  self.client_address
        if hasattr(self, 'log_urls') and ip not in self.log_urls:
            self.raw_requestline = self.rfile.readline()
            if self.parse_request(): self.send_error(403)
        else:
            self.__base_handle()

    def _connect_to(self, netloc, soc):
        i = netloc.find(':')
        if i >= 0:
            host_port = netloc[:i], int(netloc[i+1:])
        else:
            host_port = netloc, 80
        print "\t" "connect to %s:%d" % host_port
        try: soc.connect(host_port)
        except socket.error, arg:
            try: msg = arg[1]
            except: msg = arg
            self.send_error(404, msg)
            return 0
        return 1

    def do_CONNECT(self):
        soc = socket.socket()
        try:
            if self._connect_to(self.path, soc):
                self.log_request(200)
                self.wfile.write(self.protocol_version +
                                 " 200 Connection established\r\n")
                self.wfile.write("Proxy-agent: %s\r\n" % self.version_string())
                self.wfile.write("\r\n")
                self._read_write(soc, 300)
        finally:
            print "\t" "bye"
            soc.close()
            self.connection.close()

    def do_GET(self):
        (scm, netloc, path, params, query, fragment) = urlparse.urlparse(self.path, 'http')
        if scm != 'http' or fragment or not netloc:
            self.send_error(400, "bad url %s" % self.path)
            return
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            i = netloc.find(':')
            if i == -1 :
                port= 80
                host = netloc
            else:
                port = int(netloc[i+1:])
                host = netloc[:i]
            self.log_request()
            print repr(self.headers)
            self.headers['Connection'] = 'close'
            del self.headers['Proxy-Connection']
            header = '\r\n'.join(self.headers.headers)
            if query :
                netloc += '?'
                netloc += query
            request = '%s %s %s\r\n%s\r\n\r\n'%(self.command, path, self.version_string, header)
            data = ''
            if self.command in ['POST']:
                i = int(self.headers.getheader('Content-Length'))
                data = self.rfile.read(i)
            request += data
            recv = self.proxy((host,port), request)
            #todo
        finally:
            print "\t" "bye"
            soc.close()
            self.connection.close()
            
    def proxy(self, host ,request):
        try:
            rec = ""
            soc = socket.create_connection(host)
            soc.send(request)
            soc.settimeout(5)
            data = soc.recv(2048)
            rec = data
            while len(data) == 2048:
                data = soc.recv(2048)
                rec += data
        except socket.timeout:
            if rec == "":
                self.send_error(404 ,"Request Time Out -- by pyProxy")
                return ""
            return rec
        except:
            self.send_error(400,"Unkwon -- by pyProxy")
            return ""
        return rec
        
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

    do_HEAD = do_GET
    do_POST = do_GET
    do_PUT  = do_GET
    do_DELETE=do_GET


