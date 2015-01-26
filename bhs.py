import BaseHTTPServer, select, socket, SocketServer, urlparse, httplib, shutil, cgi
class ThreadingHTTPServer (SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer): pass

class handler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        print 'GET=%s'%repr(self.headers.headers)
        print repr(self.raw_requestline)
        s = socket.socket()
        s.connect(('localhost',8080))
        s.send('hello')
        shutil.copyfileobj(s.fileno, self.wfile)
        #self.wfile.write('hello world')

    def do_POST(self):
        print 'POST=%s'%repr(self.headers.headers)
        print repr(self.raw_requestline)
        #for i in range(5):
        data = self.rfile.read(1)
        print '%i==%s=='%(0,repr(data))
            
server_address = ('', 8000)
httpd = ThreadingHTTPServer(server_address, handler)
httpd.serve_forever()
