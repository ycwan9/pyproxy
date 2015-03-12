import BaseHTTPServer, select, socket, SocketServer, urlparse, httplib

def proxy(host ,request, err_func):
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
            err_func(404 ,"Request Time Out -- by pyProxy")
            return ""
        return rec
    except:
        err_func(400,"Unkwon -- by pyProxy")
        return ""
    return rec
