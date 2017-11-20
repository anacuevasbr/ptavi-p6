#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            Message = line.decode('utf-8').split(' ')[0]
            if Message == 'INVITE':
                pass
            elif Message == 'BYE':
                pass
            elif Message == 'ACK':
                pass
            else:
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed \r\n\r\n")
            print("El cliente nos manda " + Message)

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        sys.exit('Usage: python3 server.py IP port audio_file')

    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    audio = sys.argv[3]
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    print("Listening...")
    serv.serve_forever()
