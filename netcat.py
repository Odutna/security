# -*- coding:utf-8 -*-
import sys
import argparse
from api import Client


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


def talk(client, target, port, message):
    if len(message):
        client.send(message.encode('utf-8'))
    response = client.recv()
    print(response)


def main():
    parser = build_parser()
    opt = parser.parse_args()

    if not opt.listen and len(opt.target) and opt.port > 0:
        # send received data to the target
        client = Client(opt.target, opt.port)
        try:
            while True:
                message = sys.stdin.read()
                talk(client, opt.target, opt.port, message)
        except:
            print("[*] Exception Exiging.")
            client.close()


if __name__ == '__main__':
    main()
