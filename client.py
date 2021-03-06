#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

if len(sys.argv) != 3:
    sys.exit('Usage: python3 client.py method receiver@IP:SIPport')

Method = sys.argv[1]
User = sys.argv[2].split('@')[0]
Dir = sys.argv[2].split('@')[1]
SERVER = Dir.split(':')[0]
PORT = int(Dir.split(':')[1])


# Contenido que vamos a enviar
Message = Method + ' sip:' + sys.argv[2] + ' SIP/2.0' + '\r\n\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    my_socket.send(bytes(Message, 'utf-8'))
    data = my_socket.recv(1024)
    Message = data.decode('utf-8')
    M = Message.split(' ')[1]

    if M == '100':
        Message = 'ACK sip:' + sys.argv[2] + ' SIP/2.0' + '\r\n\r\n'
        my_socket.send(bytes(Message, 'utf-8'))
