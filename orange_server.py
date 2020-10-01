#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import net_io
import random
import logging

name = 'orange_pi'
PASSWORD = '1234'

tokens = []


logging.basicConfig( level = logging.INFO )

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
sock.bind(('', 9090))
while True:    
    sock.listen(1)
    conn, addr = sock.accept()   
    
    
    while True:
      data = conn.recv(1024)
      if not data:
          break
      res = net_io.decode( data ) 
      if res['command'] == 'scan':
        output = net_io.encode( {'res':'OK', 'name':name} )
        logging.info( "Команда SCAN" )
        logging.info( "Ответ |%s|"%( output ) )
      elif res['command'] == 'login':
        if res['password'] == PASSWORD:
          token = str( random.randint( 1000000, 9999998 ) )
          logging.info( "Создан токен |%s| для адреса |%s|"%( token, addr ) )
          tokens.append( {'address':addr, 'token':token} )
          output = net_io.encode( {'res':'OK', 'token':token} )
        else:
          output = net_io.encode( {'res':'ERROR'} )
        logging.info( "Команда LOGGIN" )
        logging.info( "Ответ |%s|"%( output ) )
      elif res['command'] == 'logout':
        output = net_io.encode( {'res':'OK'} )
        
        logging.info( "Команда LOGOUT" )
        logging.info( "Ответ |%s|"%( output ) )
      else:
        output = net_io.encode( {'res':'ERROR'} )
        logging.info( "Команда UNKNOWN" )
        logging.info( "Ответ |%s|"%( output ) )
      conn.send( output )
    
    conn.close()
