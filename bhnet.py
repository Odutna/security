# -*- coding:utf-8 -*-
import argparse

from handler import TCPHandler, UDPHandler, ServerHandler


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', '--target', required=True, help='target host'
    )
    parser.add_argument(
        '-p', '--port', type=int, required=True, help='port'
    )
    parser.add_argument(
        '-u', '--udp', action='store_true', help='using udp (tcp by default)'
    )
    parser.add_argument(
        '-l', '--listen', action='store_true',
        help='listen on [host]:[port] for incoming connections'
    )
    parser.add_argument(
        '-e', '--execute', dest='file_to_run',
        help='execute the given file upon receiving a connection'
    )
    parser.add_argument(
        '-c', '--command', action='store_true', help='initialize a command shell'
    )
    parser.add_argument(
        '-U', '--upload', dest='upload_dest',
        help='upon receiving connection upload a file and write to [destination]'
    )
    options = parser.parse_args()
    return options


def make_client(opt):
    if not opt.udp:
        client = TCPHandler(opt.target, opt.port)
    else:
        client = UDPHandler(opt.target, opt.port)
    return client


def main():
    opt = parse_options()
    if not opt.listen and len(opt.target) and opt.port > 0:
        # send and receive messages with the target
        client = make_client(opt)
        client.connect()
        client.chat()
    elif opt.listen:
        # receive command from clients
        server = ServerHandler(opt.target, opt.port)
        if opt.command:
            server.wait_command()
        elif opt.upload_dest:
            pass


if __name__ == '__main__':
    main()
