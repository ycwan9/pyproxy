"""This is a tmp file for debug BaseHTTPServer simple"""
import BaseHTTPServer, select, socket, SocketServer, urlparse, httplib, shutil, cgi
class ThreadingHTTPServer (SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer): pass

class handler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        html = 'HTTP/1.1 200 OK\r\n\r\n<html><body><form method="POST"><input name="a" /><input name="s" type="submit" /></form></body></html>\r\n\r\n'
        print 'GET=%s'%repr(self.headers.headers)
        print repr(self.raw_requestline)
        #s = socket.socket()
        #s.connect(('localhost',8080))
        #s.send('hello')
        self.wfile.write(html)

    def do_POST(self):
        print 'POST=%s'%repr(self.headers.headers)
        print repr(self.raw_requestline)
        print repr(self.headers.getheader('Content-Length'))
        i = int(self.headers.getheader('Content-Length'))
        s = self.rfile.read(i)
        #s = self.rfile.readline()
        #s = self.connection.recv(1024)
        print repr(s)
        self.wfile.write(repr(s))
        #c = 'Content-Length'
        #while True:
        #    data = self.rfile.readline()
        #    print '==%s'%(repr(data))
        #    if (data == '')or(data == '\r\n'):
        #        break

server_address = ('', 8080)
print "listening in",repr(server_address)
httpd = ThreadingHTTPServer(server_address, handler)
httpd.serve_forever()