#!/usr/bin/python3
# -*- coding: utf-8 -*-


import time
import net_io
import logging


HOST = '192.168.43.87'
PORT = 9090
PASSWORD = '1234'
token = ''

cmd = { 'command':'scan', 'data':'find modules' }


logging.basicConfig( level = logging.INFO )

#res = net_io.scan_net( "192.168.43." )
res = net_io.login( HOST, PASSWORD )
if res == 'ERROR':
  logging.info( "Ошибка получения токена" )
  exit()
token = res  
net_io.logout( token )

print( res )
exit()

while True:    
  print( net_io.send_net( "127.0.0.1", cmd ) )
  time.sleep( 5 )

