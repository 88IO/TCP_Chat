#!/usr/bin/env python
# coding:utf-8 :
# Author:   881O
# Created:  2017-06-03
#
import socket
import threading
import cv2

bind_ip = "192.168.43.161"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)

#print("[*] Listening on %s:%d" % (bind_ip, bind_port))

def handle_client(client_socket):

	request = client_socket.recv(1024)
	cv2.imshow("demo", request)
#	print("[*] Received: %s" % request.decode("utf-8")) 
	
	client_socket.send(b"OK!") 
	
	client_socket.close()

while True:

	client, addr = server.accept()

#	print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

	client_handler = threading.Thread(target = handle_client, args = (client,))
	client_handler.start()

