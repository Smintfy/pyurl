import sys
import socket
import argparse
import validators
from urllib.parse import urlparse

def encode_request(method, host, path, data, header):
    # default to GET method if method not specified
    if not method:
        method = "GET"

    req = f"{method} {path} HTTP/1.1\r\n"
    req += f"Host:{host}\r\n"

    match method:
        case "GET" | "DELETE":
            req += "Accept: */*\r\n"
            req += "Connection: close\r\n\r\n"
            return req.encode()
        case "POST" | "PUT":
            req += f"{header}\r\n"
            req += f"Content-Length: {len(data)}\r\n"
            req += f"Connection: close\r\n\r\n{data}"
            return req.encode()
        case _:
            print("Error: Method doesn't exist")
            sys.exit(1)
        
def handle_request(req, host, port):
    # default to port 80 and 443 for HTTPS
    if not port:
        port = 80

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.sendall(req)

        # read the response data from the server
        res = ""
        while True:
            data = sock.recv(1024)
            if not data:
                break
            res += data.decode()
        return res
    except ValueError as err:
        print(err)
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

    if not validators.url(url):
        print('Error: provided url is not valid')
        sys.exit(1)

    parsed_url = urlparse(url)
    host, path, port = parsed_url.hostname, parsed_url.path, parsed_url.port

    # only support http for now
    if parsed_url.scheme != "http":
        print('Error: only HTTP protocol is supported')
        sys.exit(1)

    # make request with method, host name, and path
    req = encode_request(method, host, path, data, header)

    # print out the request before sending to the server if verbose flag specified
    if verbose:
        for msg in req.decode().split("\r\n"):
            print(">", msg)

    res = handle_request(req, host, port)

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