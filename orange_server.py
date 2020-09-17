#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket



sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
sock.bind(('', 9090))
while True:    
    sock.listen(1)
    conn, addr = sock.accept()   
    print( addr )
    
    while True:
        data = conn.recv(1024)
        if not data:
            break
        output = input()
                    
        conn.send( output.encode( 'utf-8' ) )
    
    conn.close()
