#!/usr/bin/env python3

# Imports
import socket
import argparse
import functions
from functions import http_handle

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-H', default='127.0.0.1', help='Select hostname')
    parser.add_argument('--port', '-p', default=8080, type=int, help='Select port number')
    args = parser.parse_args()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((args.host, args.port))
        sock.listen(1)
        print('Server listening on port', args.port)
        while True:
            with sock.accept()[0] as conn:
                request = conn.recv(1024).decode('ascii')
                reply = http_handle(request)
                conn.send(reply.encode('ascii'))
            print("\n\nReceived request")
            print("======================")
            print(request.rstrip())
            print("======================")
            print("\n\nReplied with")
            print("======================")
            print(reply.rstrip())
            print("======================")
    return 0

if __name__ == "__main__":
    main()
