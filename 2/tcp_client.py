# -*- coding:utf-8 -*-
import sys
import socket

target_host = sys.argv[1]
target_port = int(sys.argv[2])


def tcp():
    # AF_INET: IPv4, SOCK_STREAM: TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((target_host, target_port))

    # send receive raw byte strings
    client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

    response = client.recv(4096)

    # decode bytes to strings
    print(response.decode())


def udp():
    # AF_INET: IPv4, SOCK_DGRAM: TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client.sendto(b"AAABBBCCC", (target_host, target_port))

    data, addr = client.recvfrom(4096)

    # decode bytes to strings
    print(data.decode())

tcp()
udp()
