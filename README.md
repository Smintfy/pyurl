# pyurl

`GET`
```bash
% python main.py http://eu.httpbin.org/get
{
  "args": {},
  "headers": {
    "Accept": "*/*",
    "Host": "eu.httpbin.org",
    "X-Amzn-Trace-Id": "Root=1-6603c705-72ac04a052de6c9120da5385"
  },
  "url": "http://eu.httpbin.org/get"
}
```

`GET` with -v (verbose)
> ">" and "<" to show which direction the message went
```bash
% python main.py -v http://eu.httpbin.org/get
> GET /get HTTP/1.1
> Host:eu.httpbin.org
> Accept: */*
> Connection: close
>
>
< HTTP/1.1 200 OK
< Date: Wed, 27 Mar 2024 07:13:27 GMT
< Content-Type: application/json
< Content-Length: 224
< Connection: close
< Server: gunicorn/19.9.0
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Credentials: true
<
{
  "args": {},
  "headers": {
    "Accept": "*/*",
    "Host": "eu.httpbin.org",
    "X-Amzn-Trace-Id": "Root=1-6603c717-14724a9927f146036884fb4d"
  },
  "url": "http://eu.httpbin.org/get"
}
```

`DELETE`
```bash
{
  "args": {},
  "data": "",
  "files": {},
  "form": {},
  "headers": {
    "Accept": "*/*",
    "Host": "eu.httpbin.org",
    "X-Amzn-Trace-Id": "Root=1-6603c80d-204dc6541afcf2dc43ce2f38"
  },
  "json": null,
  "url": "http://eu.httpbin.org/delete"
}
```
