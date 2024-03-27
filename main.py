import sys
import socket
import argparse
import validators
from urllib.parse import urlparse

def encode_request(host, path):
    # fields are separated by \r\n and the request ends with \r\n\r\n
    req = f"GET {path} HTTP/1.1\r\n"
    req += f"Host:{host}\r\n"
    req += "Accept: */*\r\n"
    req += "Connection: close\r\n\r\n"

    # encode from string to bytes
    return req.encode()

# send the GET request and dump out the response
def send_GET(host, path, port=80):
    try:
        # socks :D    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(encode_request(host, path))

        res = ""

        # read the data from the server
        while True:
            data = sock.recv(1024)
            if not data:
                print("Error reading data")
                break
            res += data.decode()
        return res
    except ValueError as err:
        print(err)
        sys.exit(1)

def main():
    # -X <method>
    # url
    parser = argparse.ArgumentParser()

    parser.add_argument("-X")
    parser.add_argument("url")

    args = parser.parse_args()

    print(args.X, args.url)
    
    url = args.url

    if not validators.url(url):
        print('Error: provided url is not valid')
        sys.exit(1)

    parsed_url = urlparse(url)

    if parsed_url.scheme != "http":
        print('Error: only HTTP protocol is supported')
        sys.exit(1)

    res = send_GET(parsed_url.hostname, parsed_url.path)
    print(res)

if __name__ == "__main__":
    main()