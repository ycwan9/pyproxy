# -*- coding: utf-8 -*-
import BaseHTTPServer, select, socket, SocketServer, urlparse, httplib
import handler
import Queue

class ThreadingHTTPServer (SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer): pass
print 'a'
if __name__ == '__main__':
    print 'hello'
    from sys import argv
    if argv[1:] and argv[1] in ('-h', '--help'):
        print argv[0], "[port [log_url_name ...]]"
    else:
        port = 8080
        if argv[1:]:
            port = int(argv[1])
        print "listen on %i"%port
        req_queue = Queue.Queue()
        httpd = ThreadingHTTPServer(('0.0.0.0',port), handler.ProxyHandler)
        httpd.serve_forever()