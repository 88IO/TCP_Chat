#!/usr/bin/env python
# coding:utf-8 :
# Author:   881O
# Created:  2017-06-03
#
import socket
import threading
import getopt
import sys


def usage():
    print()
    print("tcp_server.exe --port = <PORT-NUMBER>")
    print()


def version():
    print("Version: 0.0.1")
    print()


def tcp_server(bind_ip, bind_port):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((bind_ip, bind_port))

    server.listen(5)

    print("[*] Listening on %s:%d\n" % (bind_ip, bind_port))

    def handle_client(client_socket):

        request = client_socket.recv(1024)

        print("%s" % request.decode("utf-8"))

        client_socket.send(b"")

        client_socket.close()

    while True:

        client, addr = server.accept()

        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def main():
    bind_ip = socket.gethostbyname(socket.gethostname())
    bind_port = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:hv", [
                                   "port=", "help", "version"])
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
        if o in ("-p", "--port"):
            bind_port = a

    if bind_port is None:
        usage()
        sys.exit(0)

    print("Bind_IP:   %s" % (bind_ip,))
    print("Bind_PORT: %s" % (bind_port,))
    print()

    tcp_server(bind_ip, int(bind_port))


if __name__ == "__main__":
    main()
