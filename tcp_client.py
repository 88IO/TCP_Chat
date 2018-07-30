#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 03:01:52 2017

@author: aoba
"""

import socket
import os
import getopt
import sys


def usage():
    print()
    print("tcp_client.exe --ip   = <IP-ADDRESS>")
    print("               --port = <PORT-NUMBER>")


def version():
    print("Version: 0.0.1")
    print()


def tcp_client(target_ip, target_port, username):

    while True:

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((target_ip, target_port))

        client.send(
            (username + " --> " + input(username + " --> ")).encode("utf-8"))

        response = client.recv(4096)

        print(response.decode("utf-8"))


def main():
    target_ip = None
    target_port = None
    username = os.environ.get("USERNAME")

    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:p:hv", [
                                   "ip=", "port=", "help", "version"])
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
        if o in ("-i", "--ip"):
            target_ip = a
        if o in ("-p", "--port"):
            target_port = a

    if (target_ip is None or target_port is None):
        usage()
        sys.exit(0)

    print("Target_IP:   %s" % (target_ip,))
    print("Target_PORT: %s" % (target_port,))
    print()

    tcp_client(target_ip, int(target_port), username)


if __name__ == "__main__":
    main()
