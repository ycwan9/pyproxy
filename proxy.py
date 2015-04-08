# -*- coding: utf-8 -*-
import BaseHTTPServer, select, socket, SocketServer, urlparse, httplib

def read_write(host, conn, err_func, request="", max_idling=20):
    print "reading & writing %s on port %i"%host
    #print "req is '%s'"%repr(request)
    try:
        rec = ""
        soc = socket.create_connection(host)
        if request:
            soc.send(request)
        #soc.send(request)
        #soc.settimeout(5)
        iw = [conn, soc]
        count = 0
        istr = ''
        ostr = ''
        while 1:
            count += 1
            (ins, _, exs) = select.select(iw, [], iw, 3)
            if exs: break
            if ins:
                for i in ins:
                    if i is soc:
                        out = conn
                        s = ostr
                    else:
                        out = soc
                        s = istr
                    data = i.recv(8192)
                    if data:
                        out.send(data)
                        s += data
                        count = 0
            else:
                print "\t" "idle", count
            if count == max_idling: break
    except socket.timeout:
        if request == "":
            return rec
        if rec == "":
            err_func(404 ,"Request Time Out -- by pyProxy")
            return 0
        return rec
    except:
        err_func(400,"Unkwon -- by pyProxy")
        return 0
    print 'input ===\n%s\n'%istr
    print 'output ===\n%s\n'%ostr
    return rec

def proxy(host, conn, err_func, request):
    #print "proxying %s on port %i"%host
    #print "req is '%s'"%repr(request)
    try:
        soc = socket.create_connection(host)
        soc.send(request)
        fd = soc.makefile()
        data = fd.readline()
        buf = ""
        con_len = -1
        while buf != '\r\n':
            data += buf
            if buf.find('Content-Length') != -1:
                con_len = int(buf[buf.find(':')+1:])
            buf = fd.readline()
        if con_len != -1:
            data += fd.read(con_len)
            conn.send(data)
        else:
            #soc.settimeout(10)
            #buf = ''
            #while buf != '\r\n':
            #    buf = fd.readline()
            #    data += buf
            ##todo
            soc.settimeout(1)
            conn.send(data)
            buf = soc.recv(2048)
            conn.send(buf)
            data += buf
            while len(buf) == 2048:
                buf = soc.recv(2048)
                conn.send(buf)
                data += buf
    except socket.timeout:
        if request == "":
            return data
        if data == "":
            err_func(404 ,"Request Time Out -- by pyProxy")
            return 0
        return data
    #except:
    #    err_func(400,"Unkwon -- by pyProxy")
    #    return 0
    return data
