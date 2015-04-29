import Queue
format = """==========================
%s
==========================
%s
==========================
"""
def do_debug(path, query, wfile, req_queue, err_func):
    if path == '/':
        s = req_queue.qsize()
        rep = ""
        if s < 1 :
            rep = "There are any HTTP data right now\n"
        else:
            for i in range(s):
                q, r = req_queue.get_nowait()
                rep += format%(repr(q), repr(r))
        wfile.write("""HTTP/1.1 200 OK\r\n\r\n%s\r\n\r\n"""%rep)
        return
    else:
        err_func(404, "pyProxy Debug Module v0.1, file not found")