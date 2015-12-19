# -*- coding:utf-8 -*-
import socket

MAX_SIZE = 4096


class Client(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.handler = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

    def connect(self):
        self.handler.connect((self.host, self.port))

    def send(self, message):
        self.handler.send(message)

    def recv(self):
        response = self.handler.recv(MAX_SIZE)
        return response

    def close(self):
        self.handler.close()
