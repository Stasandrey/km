#!/usr/bin/python3
# -*- coding: utf-8 -*-

import client_API
import logging
import time

HOST = '192.168.43.87'
PORT = 9090
PASSWORD = '1234'
token = ''

logging.basicConfig( level = logging.INFO )

res = client_API.login( HOST, PASSWORD )
if res['result'] == 'ERROR':
  logging.info( "Ошибка получения токена" )
  exit()
token = res['data']['token']  

#client_API.change_filename( HOST, token, 'out6.cod' )
#client_API.get_filelist( HOST, token )
#res = client_API.get_file( HOST, token, 'out.cod' )

client_API.get_translate( HOST, token )
client_API.set_translate( HOST, token, 'ON' )
client_API.get_translate( HOST, token )
while True:
  res = client_API.get_barcode( HOST, token )
  if res['result'] == 'OK':
    print( "Barcode:[%s]"%( res['data'] ) )
  time.sleep( 5 )
client_API.logout( HOST, token )

print( res )



