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

    def talk(self):
        try:
            while True:
                print("[*] Input: ", end='')
                sys.stdout.flush()
                message = sys.stdin.read()
                if message:
                    self.send(message.encode(ENCODE))
                response = self.recv()
                print(response.decode(ENCODE))
        except:
            print("[*] Exception Exiging.")
            traceback.print_exc(file=sys.stdout)


class TCPHandler(AbstractHandler):
    def __init__(self, host, port):
        super().__init__(host, port)
        # AF_INET: IPv4, SOCK_STREAM: TCP
        self.handler = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.handler.connect((host, port))

    def __del__(self):
        self.handler.close()

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


class ServerHandler(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # AF_INET: IPv4, SOCK_STREAM: TCP
        self.handler = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.handler.bind((host, port))

    def listen(self):
        self.handler.listen(MAX_CONNECTION)
        print("[*] Listening on {}:{}".format(self.host, self.port))
        self.accept()

    def accept(self):
        while True:
            client, addr = self.handler.accept()
            print("[*] Accepted connection from: {}:{}".format(addr[0], addr[1]))
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def handle_client(self, client_socket):
        request = client_socket.recv(MAX_SIZE)
        print("[*] Command Received '{}'".format(request.decode(ENCODE).rstrip()))
        output = self.run_command(request)
        print("[*] Command Executed")
        client_socket.send(output)
        client_socket.close()

    def run_command(self, command):
        command = command.rstrip()
        try:
            output = subprocess.check_output(
                command, stderr=subprocess.STDOUT, shell=True
            )
        except:
            output = "Failed to execute command."
        return output
