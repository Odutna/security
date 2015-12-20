# -*- coding:utf-8 -*-
import abc
import socket

MAX_SIZE = 4096
ENCODE = 'utf-8'


class AbstractHandler(metaclass=abc.ABCMeta):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @abc.abstractmethod
    def send(self):
        pass

    @abc.abstractmethod
    def recv(self):
        pass

    def talk(self, message):
        if message:
            self.send(message.encode(ENCODE))
        response = self.recv()
        print(response.decode(ENCODE))


class TCPHandler(AbstractHandler):
    def __init__(self, host, port):
        super().__init__(host, port)
        # AF_INET: IPv4, SOCK_STREAM: TCP
        self.handler = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.connect()

    def __del__(self):
        self.handler.close()

    def connect(self):
        self.handler.connect((self.host, self.port))

    def send(self, message):
        self.handler.send(message)

    def recv(self):
        response = self.handler.recv(MAX_SIZE)
        return response

    def close(self):
        self.handler.close()


class UDPHandler(AbstractHandler):
    def __init__(self, host, port):
        super().__init__(host, port)
        # AF_INET: IPv4, SOCK_DGRAM: UDP
        self.handler = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM
        )

    def send(self, message):
        self.handler.sendto(message, (self.host, self.port))

    def recv(self):
        data, addr = self.handler.recvfrom(MAX_SIZE)
        return data
