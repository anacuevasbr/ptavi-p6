#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import os
import socketserver
import sys


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            Message = line.decode('utf-8').split(' ')
            Method = str(Message[0])
            if Method != '':
                if len(Message) == 3 and str(Message[2].split("/")[0]) == 'SIP':
                    if Method == 'INVITE':
                        line = ('SIP/2.0 100 Trying \r\n\r\n'
                                + 'SIP/2.0 180 Ringing \r\n\r\n'
                                + 'SIP/2.0 200 OK \r\n\r\n')
                        self.wfile.write(bytes(line, 'utf-8'))
                    elif Method == 'BYE':
                        line = ('SIP/2.0 200 OK \r\n\r\n')
                        self.wfile.write(bytes(line, 'utf-8'))
                    elif Method == 'ACK':
                        audio = sys.argv[3]
                        order = "./mp32rtp -i 127.0.0.1 -p 23032 < " + audio
                        os.system(order)
                    else:
                        self.wfile.write(b"SIP/2.0 405 Method Not Allowed \r\n\r\n")
                    print("El cliente nos manda " + str(Message[0]))
                else:
                    self.wfile.write(b"SIP/2.0 400 Bad Request \r\n\r\n")

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        sys.exit('Usage: python3 server.py IP port audio_file')

    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    print("Listening...")
    serv.serve_forever()
