# pyurl

A curl clone toy project written in python for testing REST API with HTTP/1.1 protocol. Support localhost, HTTP, and HTTPS.

## TODO
- [ ] Handling keep alive and using it to send multiple requests over the same TCP connection.
- [ ] Graphical User Interface
- [ ] Automated API testing

## Get started
1. Clone the repository

   ```bash
    git clone https://github.com/Smintfy/link-shortener-node.git
   ```
2. Create a virtual environment

    ```bash
    python -m venv pyurl
   ```
3. Install the requirements
   
   ```bash
   pip install -r requirements.txt
   ```

4. Run the program
   
   ```bash
   python main.py
   ```

## Methods
enable -v flag to enable verbose (adding > and < to show which direction the message went)

`GET`
```bash
   python pycurl.py http://eu.httpbin.org/get

   # output

   {
        "args": {},
        "headers": {
            "Accept": "*/*",
            "Host": "eu.httpbin.org",
            ...
        },
        "url": "http://eu.httpbin.org/get"
    }
```

`DELETE`
```bash
   python pycurl.py -X DELETE http://eu.httpbin.org/delete

   # output

   {
        "args": {},
        "data": "",
        "files": {},
        "form": {},
        "headers": {
            "Accept": "*/*",
            "Host": "eu.httpbin.org",
            ...
        },
        "json": null,
        "url": "http://eu.httpbin.org/delete"
    }
```

`POST`
```bash
   python pycurl.py -X POST http://eu.httpbin.org/post \
    -d '{"key": "value"}' \
    -H "Content-Type: application/json"

    # output

    {
        "args": {},
        "data": "{\"key\": \"value\"}",
        "files": {},
        "form": {},
        "headers": {
            "Content-Length": "16",
            "Content-Type": "application/json",
            "Host": "eu.httpbin.org",
            ...
        },
        "json": {
            "key": "value"
        },
        "url": "http://eu.httpbin.org/post"
    }
```

`PUT`
```bash
   python pycurl.py -X PUT http://eu.httpbin.org/put \
    -d '{"key": "value2"}' \
    -H "Content-Type: application/json"

    # output

    {
        "args": {},
        "data": "{\"key\": \"value2\"}",
        "files": {},
        "form": {},
        "headers": {
            "Content-Length": "17",
            "Content-Type": "application/json",
            "Host": "eu.httpbin.org",
            ...
        },
        "json": {
            "key": "value2"
        },
        "url": "http://eu.httpbin.org/put"
    }
```
