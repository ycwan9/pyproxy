__version__ = "0.1"

import BaseHTTPServer, select, socket, SocketServer, urlparse, httplib
import handler

class ThreadingHTTPServer (SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer): pass

if __name__ == '__main__':
    from sys import argv
    if argv[1:] and argv[1] in ('-h', '--help'):
        print argv[0], "[port [log_url_name ...]]"
    else:
        port = 8080
        if argv[1:]:
            port = int(argv[1])
        print "listen on %i"%port
        httpd = BaseHTTPServer.HTTPServer(('0.0.0.0',port), handler.ProxyHandler)
        httpd.serve_forever()
