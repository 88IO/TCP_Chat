#!/usr/bin/env python
# coding:   utf-8
# Author:   881O
# Created:  2018-07-27
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
    print("tcp.exe  --ip      = <IP-ADDRESS>")
    print("         --port    = <PORT-NUMBER>")
    print("         --server  = <SERVER-MODE>")
    print("         --command = <COMMAND-MODE>")
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

        response = client_socket.recv(4096).decode("shift-jis")
        print(response)

        if command_mode:
            request = input("CMD >> ")
            try:
                client_socket.send(request.encode("shift-jis"))
            except:
                print("Cannot send command...")
            if request == "exit":
                print("Exit...")
        else:
            request = input("MSG >> ")
            client_socket.send(request.encode("shift-jis"))

        client_socket.close()

    while True:

        client, addr = server.accept()

        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def tcp_client(target_ip, target_port, username, command_mode):

    request = "chdir"
    response = "<<%s>>\n" % username 

    print("Connected...")

    while True:

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((target_ip, target_port))

        if command_mode:
            if request == "exit":
                client.close()
                print("Exit...")
                sys.exit(0)
            else:
                try:
                    client.send(response.encode("shift-jis") 
                                + subprocess.check_output(request, stderr=subprocess.STDOUT, shell=True))
                except:
                    client.send(
                        "内部コマンドまたは外部コマンド、またはバッチ ファイルとして認識されていません。".encode("shift-jis"))
        else:
            request = "OK"
            response = "\n"
            print(request)
            client.send(response.encode("shift-jis"))
            
        request = client.recv(4096).decode("shift-jis")


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

    if (ip_address is None or port_num is None):
        usage()
        sys.exit()

    print("IP_ADDRESS:   %s" % (ip_address,))
    print("PORT_NUM:     %s" % (port_num,))
    print("SERVER_MODE:  %s" % (server_mode,))
    print("COMMAND_MODE: %s" % (command_mode,))
    print()

    if server_mode is True:
        tcp_server(ip_address, int(port_num), username, command_mode)
    else:
        tcp_client(ip_address, int(port_num), username, command_mode)


if __name__ == "__main__":
    main()
