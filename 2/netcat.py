# -*- coding:utf-8 -*-
import sys
import argparse
import socket


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', '--target', required=True, help='target host'
    )
    parser.add_argument(
        '-p', '--port', type=int, required=True, help='port'
    )
    parser.add_argument(
        '-l', '--listen',  help='listen on [host]:[port] for incoming connections'
    )
    parser.add_argument(
        '-e', '--execute', dest='file_to_run',
        help='execute the given file upon receiving a connection'
    )
    parser.add_argument(
        '-c', '--command', help='initialize a command shell'
    )
    parser.add_argument(
        '-u', '--upload', dest='destination',
        help='upon receiving connection upload a file and write to [destination]'
    )
    return parser


def client_sender(target, port, buffer):
    # AF_INET: IPv4, SOCK_STREAM: TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer.encode())

        while True:
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += str(data)

                if recv_len < 4096:
                    break

                buffer = raw_input("")
                buffer += "\n"

                client.send(buffer.encode())
    except:
        print("[*] Exception Exiging.")

        client.close()


def main():
    parser = build_parser()
    opt = parser.parse_args()

    if not opt.listen and len(opt.target) and opt.port > 0:
        # send received data to the target
        buffer = sys.stdin.read()
        client_sender(opt.target, opt.port, buffer)


if __name__ == '__main__':
    main()
