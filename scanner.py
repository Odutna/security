# -*- coding:utf-8 -*-
import os
import socket
import atexit
import struct
import threading
from ctypes import (
    Structure,
    c_ubyte,
    c_ushort,
    c_ulong,
    sizeof,
)
from netaddr import IPNetwork, IPAddress

from utils import until_interrupt
from handler import UDPClientHandler

MAX_SIZE = 65565


class IP(Structure):
    _fields_ = [
        ("ihl",           c_ubyte, 4),
        ("version",       c_ubyte, 4),
        ("tos",           c_ubyte),
        ("len",           c_ushort),
        ("id",            c_ushort),
        ("offset",        c_ushort),
        ("ttl",           c_ubyte),
        ("protocol_num",  c_ubyte),
        ("sum",           c_ushort),
        ("src",           c_ulong),
        ("dst",           c_ulong)
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        # map protocol constants to their names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

        # human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        # human readable protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)


class ICMP(Structure):
    _fields_ = [
        ("type",         c_ubyte),
        ("code",         c_ubyte),
        ("checksum",     c_ushort),
        ("unused",       c_ushort),
        ("next_hop_mtu", c_ushort)
        ]

    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass


class Scanner(object):
    probe = 'PYTHONRULES!'

    def __init__(self, host, subnet):
        self.host = host
        self.subnet = subnet
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

    def scan(self):
        @until_interrupt
        def _scan():
            raw_buffer = self.recv()[0]
            ip_header = IP(raw_buffer[0:20])
            # print("Protocol: {} {} -> {}".format(
            #     ip_header.protocol, ip_header.src_address, ip_header.dst_address
            # ))

            # if it's ICMP we want it
            if ip_header.protocol == "ICMP":
                # calculate where our ICMP packet starts from ip header length
                offset = ip_header.ihl * 4
                buf = raw_buffer[offset:offset + sizeof(ICMP)]

                # create our ICMP structure
                icmp_header = ICMP(buf)
                # print('ICMP -> Type: {:d} Code: {:d}'.format(icmp_header.type, icmp_header.code))

                get_probe = lambda x: x[len(x)-len(self.probe):].decode()
                if icmp_header.code == 3 and icmp_header.type == 3:
                    if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                        if get_probe(raw_buffer) == self.probe:
                            print('Host UP: {}'.format(ip_header.src_address))

        self.send_probe()
        _scan()

    def send_probe(self):
        """send UDP packet to the whole subnet"""
        sender = UDPClientHandler()

        def _send():
            for ip in IPNetwork(self.subnet):
                try:
                    sender.send(self.probe, host=str(ip), port=65212)
                except:
                    pass

        t = threading.Thread(target=_send)
        t.start()


if __name__ == '__main__':
    host = '192.168.128.225'
    subnet = '192.168.128.0/24'
    scanner = Scanner(host, subnet)
    print('[*] Scan Starting...')
    scanner.scan()
