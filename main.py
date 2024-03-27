import sys
import socket
import argparse
import validators
from urllib.parse import urlparse

def encode_request(method, host, path):
    # Connection: close -> tell server to close the connection
    req = f"{method} {path} HTTP/1.1\r\n"
    req += f"Host:{host}\r\n"
    req += "Accept: */*\r\n"

    match method:
        case "GET" | "DELETE":
            req += "Connection: close\r\n\r\n"
            # encode from string to bytes
            return req.encode()
        case _:
            print("Error: Method doesn't exist")
            sys.exit(1)

# send request and dump out the response
def handle_request(req, host, port=80):
    try:
        # socks :D 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(req)

        res = ""

        # read the data from the server
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
    # -v verbose > in, < out
    # -X <method>
    # url
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", action="store_true")
    parser.add_argument("-X")
    parser.add_argument("url")

    args = parser.parse_args()
    url = args.url

    if not validators.url(url):
        print('Error: provided url is not valid')
        sys.exit(1)

    parsed_url = urlparse(url)

    if parsed_url.scheme != "http":
        print('Error: only HTTP protocol is supported')
        sys.exit(1)

    method = args.X or "GET"

    req = encode_request(method, parsed_url.hostname, parsed_url.path)

    # verbose req, incoming direction
    if args.v:
        for item in req.decode().split("\r\n"):
            print(">", item)
    else:
        print(req.decode())

    res = handle_request(req, parsed_url.hostname)

    # verbose response, outcome direction
    if args.v:
        for item in res.split("\r\n"):
            if not item.startswith("{"):
                print("<", item)
            else:
                print(item)
    else:
        print(res)
        

if __name__ == "__main__":
    main()