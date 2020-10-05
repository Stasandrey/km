#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import diff_func

diff_func.DEBUG_API = True
diff_func.DEBUG_NET_IO = True
PORT = 9090

#logging.basicConfig( level = logging.INFO )
#*******************************************************************************
# Реализация API
# Возвращает кодированный  объект для передачи по сокету


# Отправляет объект на сокет и возвращает {'result':'OK'/'ERROR', 'res':result}
def send_net( addr, cmd, data ):
  print( addr )
  with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as sock:
    try:
      sock.connect(( addr, PORT ))
    except:
      return {'result':'ERROR', 'data':'socket_error'}
    else:
      p = { 'command':cmd, 'data':data }
      j_cmd = diff_func.encode( p )
      sock.sendall( j_cmd )
      data = sock.recv(1024)
      res = diff_func.decode( data )
      return { 'result':res['result'], 'data':res['data'] }
      
# Возвращает список адресов с доступными серверами 
# input     '192.168.1.'   
# output    {'address':'168.1.1.10', 'name':'Имя'}  
@diff_func.log
def scan_net( addr ):
  res = []
  for i in range( 250 ):
    host = addr + str( i + 1 )
    r = send_net( host, 'scan', '' )
    if r['result'] == 'OK':
      res.append( {'address':host, 'name':r['data']['name']} )
  return res  

# Подключение к сокету сервера по паролю. Сервер выдает токен для дальнейшей
# коммуникации
@diff_func.log
def login( addr, password ):
  return send_net( addr, 'login', { 'password':password } )
  
# Отключение от сокета сервера. Сервер переходит в состояние считывания кодов
@diff_func.log
def logout( addr, token ):
  send_net( addr, 'logout', { 'token':token } )
  return 'OK'

# Изменение файла для записи считанных кодов
@diff_func.log
def change_filename( addr, token, name ):
  return send_net( addr, 'change_filename', { 'token':token, 
                                          'filename':name } )
  
# Получить список файлов с кодами
@diff_func.log
def get_filelist( addr, token ):
  return send_net( addr, 'get_filelist', { 'token':token } )

# Загрузить определенный файл
@diff_func.log
def get_file( addr, token, filename ):
  return send_net( addr, 'get_file', { 'token':token, 'filename':filename } )

# Получить имя текущей сессии
@diff_func.log
def get_current( addr, token ):
    return send_net( addr, 'get_current', { 'token':token } )
 
# Установить режим передачи данных
@diff_func.log
def set_translate( addr, token, on_off ):
  return send_net( addr, 'set_translate', { 'token':token, 'flag':on_off } )

# Прочитать режим передачи данных
@diff_func.log
def get_translate( addr, token ):
  return send_net( addr, 'get_translate', { 'token':token } )

# Получить код от сервера
@diff_func.log
def get_barcode( addr, token ):
  return send_net( addr, 'get_barcode', { 'token':token } )
