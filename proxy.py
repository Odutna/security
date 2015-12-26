import argparse

from handler import ServerHandler


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('localhost', required=True, help='local host')
    parser.add_argument('localport', required=True, type=int, help='local port')
    parser.add_argument('remotehost', required=True, help='remote host')
    parser.add_argument('remoteport', required=True, type=int, help='remote port')
    parser.add_argument('receive_first', default=False, help='receive_first')
    options = parser.parse_args()
    return options


def main():
    opt = parse_options()
    server = ServerHandler(opt.localhost, opt.localport)
    server.proxy(opt.remotehost, opt.remoteport, opt.receive_first)

if __name__ == '__main__':
    main()
