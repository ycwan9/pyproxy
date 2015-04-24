#This file was originally generated by PyScripter's unitest wizard

import unittest
import proxy
import Queue

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
        conn = debug_conn()
        req='GET http://w3school.com.cn/index.html HTTP/1.1\r\nHost:w3school.com.cn\r\n\r\n'
        proxy.proxy(host, conn, conn.error, req, q)
        rec = conn.rec
        mylen = len(rec[rec.find('\r\n\r\n')+4:])
        headlen = 0
        i = rec.find('Content-Length')
        if i != -1:
            lenstr = rec[i+15:i+25]
            lenstr = lenstr[:lenstr.find('\r')]
            headlen = int(lenstr)
        self.assertEqual(mylen,headlen)

class debug_conn():
    def __init__(self):
        self.rec = ''
        self.err = []

    def send(self, a):
        print """========
        %s
        ========"""%repr(a)
        self.rec += a

    def error(self, v, s):
        print 'code: %s, message: %s\n'%(v,s)
        self.err += (v,s)



if __name__ == '__main__':
    unittest.main()