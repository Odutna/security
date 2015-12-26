import argparse

from handler import ServerHandler


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('localhost', help='local host')
    parser.add_argument('localport', type=int, help='local port')
    parser.add_argument('remotehost', help='remote host')
    parser.add_argument('remoteport', type=int, help='remote port')
    parser.add_argument('--receive_first', action="store_true", help='receive_first')
    options = parser.parse_args()
    return options


def main():
    opt = parse_options()
    server = ServerHandler(opt.localhost, opt.localport)
    server.proxy(opt.remotehost, opt.remoteport, opt.receive_first)

if __name__ == '__main__':
    main()
