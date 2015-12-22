# -*- coding:utf-8 -*-
import sys
import traceback
import abc
import socket
import threading
import subprocess

MAX_SIZE = 4096
MAX_CONNECTION = 5
ENCODE = 'utf-8'
PROMPT = b'<BHP:#> '


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

    def recv_data(self):
        """receive all data by loop"""
        data = ''
        while True:
            response = self.recv()
            if len(response) < MAX_SIZE:
                return data + response.decode(ENCODE)
            else:
                data += response.decode(ENCODE)

    def chat(self):
        try:
            while True:
                message = sys.stdin.read()
                if message:
                    self.send(message.encode(ENCODE))
                response = self.recv_data()
                print(response)
        except:
            print("[*] Exception Exiging.")
            traceback.print_exc(file=sys.stdout)


class TCPHandler(AbstractHandler):
    def __init__(self, host, port, handler=None):
        super().__init__(host, port)
        # AF_INET: IPv4, SOCK_STREAM: TCP
        self.handler = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) if not handler else handler

    def __del__(self):
        self.handler.close()

    def connect(self):
        self.handler.connect((self.host, self.port))

    def send(self, message):
        self.handler.send(message)

    def recv(self):
        return self.handler.recv(MAX_SIZE)

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


class ServerHandler(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # AF_INET: IPv4, SOCK_STREAM: TCP
        self.handler = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.handler.bind((host, port))
        self.listen()

    def listen(self):
        self.handler.listen(MAX_CONNECTION)
        print("[*] Listening on {}:{}".format(self.host, self.port))

    def wait_command(self):
        print("[*] Waiting Command")
        while True:
            client, addr = self.handler.accept()
            print("[*] Accepted connection from: {}:{}".format(*addr))
            client_handler = threading.Thread(
                target=self.shell, args=(TCPHandler(*addr, handler=client),)
            )
            client_handler.start()

    def shell(self, client):
        while True:
            client.send(PROMPT)
            request = client.recv_data()
            print("[*] Command Received '{}'".format(request.rstrip()))
            output = self.run_command(request)
            print("[*] Command Executed")
            client.send(output)

    def run_command(self, command):
        command = command.rstrip()
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except:
            output = b"Failed to execute command"
        return output
