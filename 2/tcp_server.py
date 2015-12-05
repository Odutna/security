# -*- coding:utf-8 -*-

import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999


def run_server():
    # AF_INET: IPv4, SOCK_STREAM: TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((bind_ip, bind_port))

    # max connections: 5
    server.listen(5)

    print("[*] Listening on {}:{}".format(bind_ip, bind_port))

    while True:
        client, addr = server.accept()

        print("[*] Accepted connection from: {}:{}".format(addr[0], addr[1]))

        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def handle_client(client_socket):
    request = client_socket.recv(1024)

    print("[*] Received {}".format(request))

    client_socket.send(b"ACK!")
    client_socket.close()

run_server()
