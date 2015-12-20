# -*- coding:utf-8 -*-
import sys
import traceback
import argparse

from handler import TCPHandler, UDPHandler


def build_parser():
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
        '-U', '--upload', dest='destination',
        help='upon receiving connection upload a file and write to [destination]'
    )
    return parser


def make_client(opt):
    if not opt.udp:
        client = TCPHandler(opt.target, opt.port)
    else:
        client = UDPHandler(opt.target, opt.port)
    return client


def main():
    parser = build_parser()
    opt = parser.parse_args()

    if not opt.listen and len(opt.target) and opt.port > 0:
        # send and receive messages with the target
        client = make_client(opt)
        try:
            while True:
                print("[*] Input: ", end='')
                sys.stdout.flush()
                # save message with line feed code
                message = sys.stdin.read()
                client.talk(message)
        except:
            print("[*] Exception Exiging.")
            traceback.print_exc(file=sys.stdout)

    elif opt.listen:
        # server_loop()
        pass


if __name__ == '__main__':
    main()
