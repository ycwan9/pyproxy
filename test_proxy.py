#This file was originally generated by PyScripter's unitest wizard

import unittest
import proxy
import Queue
import SocketServer

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testproxy(self):
        pass

    def testproxy_lenth(self):
        host = ('w3school.com.cn',80)
        q=Queue.Queue()
        fd = debug_conn()
        req='GET http://w3school.com.cn/index.html HTTP/1.1\r\nHost:w3school.com.cn\r\n\r\n'
        test = TProxy(host, req, q, fd, (lambda x,y:(self.assertTrue(0,(x,y)))))
        test.do_http()
        rec = fd.rec
        mylen = len(rec[rec.find('\r\n\r\n')+4:])
        headlen = 0
        i = rec.find('Content-Length')
        if i != -1:
            lenstr = rec[i+15:i+25]
            lenstr = lenstr[:lenstr.find('\r')]
            headlen = int(lenstr)
        self.assertEqual(mylen,headlen)
    def testproxy_queue(self):
        host = ('w3school.com.cn',80)
        q=Queue.Queue()
        fd = debug_conn()
        req='GET http://w3school.com.cn/index.html HTTP/1.1\r\nHost:w3school.com.cn\r\n\r\n'
        test = TProxy(host, req, q, fd, (lambda x,y:(self.assertTrue(0,(x,y)))))
        test.do_http()
        rec = fd.rec
        a = q.get()
        self.assertEqual(a[0],req)
        self.assertEqual(a[1],rec)
 

########################################################################
class debug_conn():
    """provide a function write() to emulate wfile.write()"""
    
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.rec = ''
        self.err = []

    def write(self, a):
        print """========
        %s
        ========"""%repr(a)
        self.rec += a
        
########################################################################
class TProxy(proxy.proxy):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, host_port, req, queue, wfile, error_func):
        """Constructor"""
        self.host_and_port = host_port
        self.request = req
        self.req_queue = queue
        self.wfile = wfile
        self.send_error = error_func
        

if __name__ == '__main__':
    unittest.main()
