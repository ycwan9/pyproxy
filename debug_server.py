import Queue
#body = """==========================
#%s
#==========================
#%s
#==========================
#"""
body = file("./debug_html/main.html").read()
css = file("./debug_html/main.css").read()
head = body[:body.find("<!--start-->")]
foot = body[body.find("<!--end-->")+10:]
body = body[body.find("<!--start-->")+12:body.find("<!--end-->")]
def do_debug(self, path):
    if path == '/':
        s = self.req_queue.qsize()
        rep = ""
        if s < 1 :
            rep = "There are any HTTP data right now\n"
        else:
            for i in range(s):
                u, q, p = self.req_queue.get_nowait()
                rep += body.format(url = u, time = "", request = q, reponse = p)
            rep = head + rep + foot
    else:
        rep = ""
        try:
            rep = file("./debug_html%s"%path).read()
        except:
            self.send_error(404, "pyProxy Debug Module v0.1, file not found")                        
            return
    self.wfile.write("""HTTP/1.1 200 OK\r\n\r\n%s\r\n\r\n"""%rep)        
    return