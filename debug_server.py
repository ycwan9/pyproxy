import Queue
def do_debug(path, query, wfile, req_queue, err_func):
    if path == '/':
        (q, r) = req_queue.get()
        wfile.write("""HTTP/1.1 200 OK\r\n\r\n
        ==========================
        %s
        ==========================
        %s
        ==========================
        \r\n\r\n"""%(repr(q), repr(r)))
        return
    else:
        err_func(404, "pyProxy Debug Module v0.1")