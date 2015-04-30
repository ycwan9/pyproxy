# -*- coding: utf-8 -*-
import httpServer, select, socket, urlparse, httplib
import handler
import Queue
import proxy

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
        proxy.proxy.req_queue = Queue.Queue()
        httpd = httpServer.ThreadingProxyHTTPServer(('0.0.0.0',port), proxy.proxy)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt,err:
            print 'bye bye\nExit by Keyboard Interrupt'%repr(err)