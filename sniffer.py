# -*- coding:utf-8 -*-
import os
import socket
import atexit

MAX_SIZE = 65565


class Sniffer(object):
    def __init__(self, host):
        self.host = host
        # create raw socket
        self.handler = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, self._choose_protocol()
        )
        # include IP header
        self.handler.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.handler.bind((host, 0))
        if self.is_windows:
            # enable promiscuous mode if Windows
            self._set_promiscuous(True)
            atexit.register(self._set_promiscuous, False)

    @property
    def is_windows(self):
        return True if os.name == 'nt' else False

    def _choose_protocol(self):
        if self.is_windows:
            return socket.IPPROTO_IP
        else:
            return socket.IPPROTO_ICMP

    def _set_promiscuous(self, enable):
        if enable:
            self.handler.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        else:
            self.handler.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

    def recv(self):
        return self.handler.recvfrom(MAX_SIZE)

if __name__ == '__main__':
    sniffer = Sniffer('192.168.0.3')
    print('[*] Capture Starting...')
    print(sniffer.recv())
