import BaseHTTPServer, select, socket, SocketServer, urlparse, httplib

def read_write(host, conn, err_func, max_idling=20):
    print "proxying %s on port %i"%host
    print "req is '%s'"%repr(request)
    try:
        rec = ""
        soc = socket.create_connection(host)
        soc.send(request)
        #soc.settimeout(5)
        iw = [conn, soc]
        count = 0
        while 1:
            count += 1
            (ins, _, exs) = select.select(iw, [], iw, 3)
            if exs: break
            if ins:
                for i in ins:
                    if i is soc:
                        out = conn
                    else:
                        out = soc
                    data = i.recv(8192)
                    if data:
                        out.send(data)
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
    return rec

def proxy(host ,request, err_func):
    print "proxying %s on port %i"%host
    print "req is '%s'"%repr(request)
    try:
        rec = ""
        soc = socket.create_connection(host)
        soc.send(request)
        #soc.settimeout(5)
        data = soc.recv(2048)
        rec = data
        while len(data) == 2048:
            data = soc.recv(2048)
            rec += data
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
    return rec
