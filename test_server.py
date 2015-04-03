import SocketServer
#a HTTP server that always respone a "hello world" message
#for debug use
class MyTCPHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline()
        print "%s wrote:%s"%(self.client_address[0], self.data)
        self.wfile.write('HTTP/1.1 200 OK\r\n\r\n<h1>hello world</h1>\r\n\r\n')

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()