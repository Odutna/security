# -*- coding:utf-8 -*-
import argparse
from getpass import getpass

from handler import TCPClientHandler, UDPClientHandler, ServerHandler, SSHClientHandler


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
        '-c', '--command', action='store_true', help='initialize a command shell'
    )
    parser.add_argument(
        '-U', '--upload', dest='upload_dest',
        help='upon receiving connection upload a file and write to [destination]'
    )
    parser.add_argument(
        '-s', '--ssh', action='store_true', dest='ssh',
        help='open ssh connection and execute command'
    )

    options = parser.parse_args()
    return options


def make_client(opt):
    if not opt.udp:
        client = TCPClientHandler(opt.target, opt.port)
    else:
        client = UDPClientHandler(opt.target, opt.port)
    return client


def main():
    opt = parse_options()
    if not opt.listen and opt.target and opt.port > 0:
        if opt.ssh:
            user = input('User: ')
            passwd = getpass()
            client = SSHClientHandler(opt.target, opt.port, user, passwd)
            client.connect()
            while True:
                command = input('Command: ')
                client.exec_command(command)
                print(client.recv_all())
        else:
            # send and receive messages with the target
            client = make_client(opt)
            client.connect()
            client.chat()
    elif opt.listen:
        # receive command from clients
        server = ServerHandler(opt.target, opt.port)
        if opt.command:
            server.shell()
        elif opt.upload_dest:
            server.upload(opt.upload_dest)

if __name__ == '__main__':
    main()
