# -*- coding: utf-8 -*-
import select, socket, urlparse, httplib
import proxyHandler
import debug_server

#def read_write(host, conn, err_func, request="", max_idling=20):
#    print "reading & writing %s on port %i"%host
#    #print "req is '%s'"%repr(request)
#    try:
#        rec = ""
#        soc = socket.create_connection(host)
#        if request:
#            soc.send(request)
#        #soc.send(request)
#        #soc.settimeout(5)
#        iw = [conn, soc]
#        count = 0
#        istr = ''
#        ostr = ''
#        while 1:
#            count += 1
#            (ins, _, exs) = select.select(iw, [], iw, 3)
#            if exs: break
#            if ins:
#                for i in ins:
#                    if i is soc:
#                        data = i.recv(8192)
#                        if data:
#                            conn.send(data)
#                            ostr += data
#                            count = 0
#                        #ostr
#                    else:
#                        data = i.recv(8192)
#                        if data:
#                            soc.send(data)
#                            istr += data
#                            count = 0
#                        #istr
#            else:
#                print "\t" "idle", count
#            if count == max_idling: break
#    except socket.timeout:
#        if request == "":
#            return rec
#        if rec == "":
#            err_func(404 ,"Request Time Out -- by pyProxy")
#            return 0
#        return rec
#    print 'input ===\n%s\n'%istr
#    print 'output ===\n%s\n'%ostr
#    return rec

class proxy(proxyHandler.ProxyHandler):
    def do_http(self):
        self.rep_data = ""
        if self.host_and_port[0] in ('debug.net', "www.debug.net"):
            self.do_debug(self.rpath)
            return
        print "proxying %s on port %s"%self.host_and_port
        try:
            soc = socket.create_connection(self.host_and_port)
            soc.send(self.request)
            fd = soc.makefile()
            data = fd.readline()
            buf = ""
            con_len = -1
            chunked = 0
            while buf != '\r\n':
                data += buf
                if buf.find('Content-Length') != -1:
                    con_len = int(buf[buf.find(':')+1:])
                if buf.find("Transfer-Encoding: chunked") != -1:
                    chunked = 1
                buf = fd.readline()
            data += "\r\n"
            soc.settimeout(10)
            if chunked :
                while buf != "0\r\n":
                    buf = fd.readline()
                    data += buf
                data += '\r\n'
            elif con_len != -1:
                print con_len
                data += fd.read(con_len)
            else:
                buf = fd.read(1024)
                while len(buf)>=1024:
                    buf = fd.read(1024)
                    data += buf
        except socket.timeout,err:
            if not data:
                self.send_error(404 ,"Request Time Out :%s -- by pyProxy"%repr(err))
                return 404
        except (socket.error,socket.herror),err:
            print repr(err)
            self.send_error(400,"Unkwon: %s -- by pyProxy"%repr(err))
            return 0
        self.wfile.write(data)
        self.req_queue.put((self.path, self.request, data))
        return
       
    def do_ssl_rw(self, max_idling=20):
        print "reading & writing %s on port %i"%self.host_and_port
        try:
            soc = socket.create_connection(self.host_and_port)
            self.wfile.write(self.protocol_version +
                             " 200 Connection established\r\n")
            self.wfile.write("Proxy-agent: %s\r\n" % self.version_string())
            self.wfile.write("\r\n")
            count = 0
            istr = '' #the input of the client's data log
            ostr = '' #the server's input(output to the client) data log
            while 1:
                count += 1
                (ins, _, exs) = select.select((soc, self.connection), (), (soc, self.connection), 3)
                if exs: break
                if ins:
                    for i in ins:
                        if i is soc:
                            data = i.recv(8192)
                            if data:
                                self.connection.send(data)
                                ostr += data
                                count = 0
                            #ostr
                        else:
                            data = i.recv(8192)
                            if data:
                                soc.send(data)
                                istr += data
                                count = 0
                            #istr
                else:
                    print "\t" "idle", count
                if count == max_idling: break
        except socket.timeout:
            print "time out, done."
            return 0
        except (socket.error,socket.herror),err:
            print "Err :%s"%repr(err)
            return 1
        self.req_queue.put((self.path, istr, ostr))
        return 0
    do_debug = debug_server.do_debug
    
