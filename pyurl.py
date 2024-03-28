import sys
import ssl
import socket
import argparse
import validators
from urllib.parse import urlparse

def encode_request(method, host, path, data, header):
    # default to GET method if method not specified
    if not method:
        method = "GET"
    
    # default data to empty string
    data = data or ""

    req = f"{method} {path} HTTP/1.1\r\n"
    req += f"Host:{host}\r\n"

    match method:
        case "GET" | "DELETE":
            req += "Accept: */*\r\n"
            req += "Connection: close\r\n\r\n"
            return req.encode()
        case "POST" | "PUT" | "PATCH":
            req += f"{header}\r\n"
            req += f"Content-Length: {len(data)}\r\n"
            req += f"Connection: close\r\n\r\n{data}" # request body
            return req.encode()
        case "HEAD":
            req += "Connection: close\r\n\r\n"
            return req.encode()
        case _:
            print("Error: Method doesn't exist")
            sys.exit(1)
        
def handle_request(req, host, protocol, port):
    if not port:
        if protocol == "https":
            port = 443
        else:
            port = 80

    try:
        # creates a TCP connection
        sock = socket.create_connection((host, port))

        # wrap the socket with ssl to support HTTPS
        if protocol == "https":
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=host)

        # send the request
        sock.sendall(req)

        # read the response data from the server
        res = ""
        while True:
            data = sock.recv(1024)
            if not data:
                break
            res += data.decode()
        return res
    except ValueError as e:
        print(e)
        sys.exit(1)
        
def main():
    parser = argparse.ArgumentParser(prog="curlpy", usage="python main.py [options...] <url>")
    parser.add_argument("-v", action="store_true", 
                        help="Enable verbose (adding > and < to show which direction the message went)")
    parser.add_argument("-X", help="Specify method, default to GET")
    parser.add_argument("url", help="<url>")
    parser.add_argument("-d", help="HTTP POST data")
    parser.add_argument("-H",help="Pass custom header(s) to server")

    args = parser.parse_args()
    verbose, method, url, data, header = args.v, args.X, args.url, args.d, args.H

    parsed_url = urlparse(url)
    host, path, protocol, port = parsed_url.hostname, parsed_url.path, parsed_url.scheme, parsed_url.port

    # validate the url and localhost
    if not validators.url(url) and not host == "localhost":
        print('Error: provided url is not valid')
        sys.exit(1)

    # only support http and https for now
    if not protocol.startswith("http"):
        print('Error: protocol not supported. Only support HTTP and HTTPS')
        sys.exit(1)

    # make request with method, host name, and path
    req = encode_request(method, host, path, data, header)

    # print out the request before sending to the server if verbose flag specified
    if verbose:
        for msg in req.decode().split("\r\n"):
            print(">", msg)

    res = handle_request(req, host, protocol, port)

    # verbose for incoming response
    if verbose:
        for msg in res.split("\r\n"):
            if not msg.startswith("{"):
                print("<", msg)
            else:
                print(msg)
        sys.exit(1)

    # default    
    print(res)

if __name__ == "__main__":
    main()