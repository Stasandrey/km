#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
HOST = '192.168.43.87'
PORT = 9090
while True:    
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

    sock.connect(( HOST, PORT ))
    s = 'hello,brother'.encode( 'utf-8' )
    sock.sendall( s )

    data = sock.recv(1024)
    print( data.decode( 'utf-8' ) )
    sock.close()


