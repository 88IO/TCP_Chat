#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 03:01:52 2017

@author: aoba
"""

import socket
import cv2

cap = cv2.VideoCapture(0)

target_host = "196.168.43.21"
target_port = 80

while cap.isOpened():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((target_host, target_port))

    client.send(cv2.read()[1])  # input("words : ").encode("utf-8"))

    response = client.recv(4096)

    print(response.decode("utf-8"))
