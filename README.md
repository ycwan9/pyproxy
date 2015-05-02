# pyproxy
- Web debug proxy writing by python
- Use "http://debug.net/" in the proxy to view the data log. 

- Usage:
<code>
python pyProxy.py [:port]
</code>

##HTTP Debug Server
- You can use http://debug.net or http://www.debug.net to view all the http request and reponse
- The debug_html/main.html is like this

- <code>
the html head & others...<br />
<!--start--\><br />
data...<br/ >
<!--stop--\><br />
other things ofthe html...
</code>
- The <code><!--start--\>...<!--stop--\></code>block will repeat many times for each request-reponse pair
- You can use <code>{url}</code> for request url
- <code>{request}</code> for the requset data
- <code>{reponse}</code> for reponse data
- <code>{time}</code> for request time (does not support this fearture now, will be added soon)