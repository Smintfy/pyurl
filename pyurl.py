import sys
import ssl
import socket
import argparse
import validators
from urllib.parse import urlparse

# protocol
HTTP = "http"
HTTPS = "https"

# localhost
LOCALHOST = "localhost"

class Sock:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host: str, protocol: str, port: int | None, verbose=False) -> None:
        # default port
        if port is None:
            if port is HTTPS:
                port = 443
            else:
                port = 80

        try:
            # create a TCP connection
            self.sock.connect((host, port))

            # wrap the connection with SSL context if protocol is HTTPS
            if protocol is HTTPS:
                context = ssl.create_default_context()
                self.sock = context.wrap_socket(self.sock, server_hostname=host)
        except:
            print(f'Error: Failed to connect to {host} port {port}: Connection refused')
            sys.exit(1)

        if verbose:
            print(f"* Connected to: {host} port {port}")

    def send(self, msg: str, verbose=False) -> None:
        if verbose:
            for header in msg.decode().split("\r\n")[:-1]:
                print(">", header)

        self.sock.sendall(msg)

    def receive(self) -> str:
        res = ""
        while True:
            data = self.sock.recv(2048)
            if not data:
                break
            res += data.decode()
        return res

def encode_request(method: str | None, host: str, path: str, data: None, header: None) -> bytes:
    # default to GET
    if method is None:
        method = "GET"

    # building the request
    req = f"{method} {path} HTTP/1.1\r\n"
    req += f"Host:{host}\r\n"
    req += "Accept: */*\r\n"
    req += "Connection: close\r\n"

    # TODO accept more than one header
    if header:
        req += f"{header}\r\n"

    # request ends with \r\n\r\n
    if data:
        req += f"Content-Length: {len(data)}\r\n"
        req += f"\r\n{data}" # request body
    else:
        req += f"\r\n"

    return req.encode()

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

    # validate url while also allowing localhost
    if url is LOCALHOST and not validators.url(url):
        print('Error: provided url is not valid')
        sys.exit(1)

    # only support HTTP and HTTPS
    if not protocol.startswith(HTTP):
        print('Error: protocol not supported. Only support HTTP and HTTPS')
        sys.exit(1)

    # initiate socket
    sock = Sock()
    sock.connect(host, protocol, port, verbose)

    req = encode_request(method, host, path, data, header)
    sock.send(req, verbose)

    res = sock.receive()

    # verbose for incoming response
    if verbose:
        for msg in res.split("\r\n")[:-1]:
            print("<", msg)

    # default    
    print(res.split("\r\n")[-1])

if __name__ == "__main__":
    main()