#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import socket
import logging

PORT = 9090

logging.basicConfig( level = logging.INFO )

# Возвращает кодированный  объект для передачи по сокету
def encode( p ):
  res = json.dumps( p ).encode( 'utf-8' )
  return res

# Возвращает раскодированный объект после приемки из сокета
def decode( p ):
  res = json.loads( p.decode( 'utf-8' ) )
  return res

# Отправляет объект на сокет и возвращает {'result':'OK'/'ERROR', 'res':result}
def send_net( addr, p ):
  print( addr )
  with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as sock:
    try:
      sock.connect(( addr, PORT ))
    except:
      return {'result':'ERROR', 'res':'socket_error'}
    else:
      j_cmd = encode( p )
      sock.sendall( j_cmd )
      data = sock.recv(1024)
      res = json.loads( data )
      return { 'result':'OK', 'res':res }
      
      
      
# Возвращает список адресов с доступными серверами 
# input     '192.168.1.'   
# output    {'address':'168.1.1.10', 'name':'Имя'}  
def scan_net( addr ):
  res = []
  for i in range( 250 ):
    host = addr + str( i + 1 )
    r = send_net( host, { 'command':'scan' } )
    if r['result'] == 'OK':
      res.append( {'address':host, 'name':r['res']['name']} )
  return res  

# Подключение к сокету сервера по паролю. Сервер выдает токен для дальнейшей
# коммуникации
def login( addr, password ):
  r = send_net( addr, { 'command':'login', 'password':password } )
  res = 'ERROR'
  if r['result'] == 'OK':
    res = r['res']['token']
  return res
  
# Отключение от сокета сервера. Сервер переходит в состояние считывания кодов
def logout( token ):
  pass
