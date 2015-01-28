import BaseHTTPServer, select, socket, SocketServer, urlparse, httplib, shutil, cgi
class ThreadingHTTPServer (SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer): pass

class handler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        print 'GET=%s'%repr(self.headers.headers)
        print repr(self.raw_requestline)
        self.rfile.seek(0)
        print repr(self.rfile.readline(65537))
        #s = socket.socket()
        #s.connect(('localhost',8080))
        #s.send('hello')
        self.wfile.write('hello world')

    def do_POST(self):
        print 'POST=%s'%repr(self.headers.headers)
        print repr(self.raw_requestline)
        print repr(self.requestline)
        while True:
            data = self.rfile.readline()
            print '==%s'%(repr(data))
            if data == '':
                break
            
server_address = ('', 8000)
httpd = ThreadingHTTPServer(server_address, handler)
httpd.serve_forever()
