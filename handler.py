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


class AbstractClientHandler(metaclass=abc.ABCMeta):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @abc.abstractmethod
    def connect(self):
        pass

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
                message = input() + '\n'
                if message:
                    self.send(bytes(message, ENCODE))
                response = self.recv_data()
                print(response.rstrip())
        except:
            print("[*] Exception Exiging.")
            traceback.print_exc(file=sys.stdout)


class TCPClientHandler(AbstractClientHandler):
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


class UDPClientHandler(AbstractClientHandler):
    def __init__(self, host, port):
        super().__init__(host, port)
        # AF_INET: IPv4, SOCK_DGRAM: UDP
        self.handler = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM
        )

    def connect(self):
        pass

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
        self.listen(MAX_CONNECTION)

    def listen(self):
        self.handler.listen(MAX_CONNECTION)
        print("[*] Listening on {}:{}".format(self.host, self.port))

    def shell(self):
        def _shell(client):
            while True:
                client.send(PROMPT)
                request = client.recv_data()
                print("[*] Command Received '{}'".format(request.rstrip()))
                output = execute(request)
                print("[*] Command Executed")
                client.send(output)

        def execute(command):
            command = command.rstrip()
            try:
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            except:
                output = b"Failed to execute command\n"
            return output

        print("[*] Waiting Command")
        while True:
            client, addr = self.handler.accept()
            print("[*] Accepted connection from: {}:{}".format(*addr))
            client_handler = threading.Thread(
                target=_shell, args=(TCPClientHandler(*addr, handler=client),)
            )
            client_handler.start()

    def upload(self, path):
        client, addr = self.handler.accept()
        client_handler = TCPClientHandler(*addr, handler=client)
        file_buffer = client_handler.recv_data()
        print("[*] Contents Received")
        try:
            file_descriptor = open(path, 'wb')
            file_descriptor.write(bytes(file_buffer, ENCODE))
            file_descriptor.close()
            client_handler.send(bytes("Successfully saved file to {}".format(path), ENCODE))
        except:
            client_handler.send(bytes("Failed saved file to {}".format(path), ENCODE))
            traceback.print_exc(file=sys.stdout)

    def proxy(self, remote_host, remote_port, receive_first):
        print("[*] Waiting Connection")
        while True:
            client, addr = self.handler.accept()
            print("[*] Accepted connection from: {}:{}".format(*addr))
            proxy_thread = threading.Thread(
                target=proxy_handler, args=(client, remote_host, remote_port, receive_first)
            )
            proxy_thread.start()
