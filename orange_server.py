#!/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
import socket
import diff_func
import server_API
import logging
import scanner
global server_run

logging.basicConfig( level = logging.INFO )

# Обработка вызовов API.
def server():
  server_API.is_server_runs = True
  sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
  sock.bind(('', 9090))
  while server_API.server_run == True:    
    sock.listen(1)
    conn, server_API.addr = sock.accept()   
    while server_API.server_run == True:
      data = conn.recv(1024)
      if not data:
          break
      res = diff_func.decode( data ) 
      if res['command'] in server_API.commands:
        if res['command'] != 'login' and res['command'] != 'scan':
          if server_API.isToken( res['data']['token'] ) != -1:
            output = server_API.commands[res['command']]( res['data'] )
          else:
            output = diff_func.encode( { 'result':'ERROR', 'data':'Bad token' } )
        else:  
          output = server_API.commands[res['command']]( res['data'] )
      else:
        output = server_API.cmd_unknown( res['data'] )
      conn.send( output )
    conn.close()
  server_API.is_server_runs = False

def read_info():
    
    while True:
      info = scanner.get_barcode()
      if server_API.read_info_run == True:
        while server_API.is_server_change_data == True:
          pass
        if server_API.read_info_write_data == True:
          server_API.is_read_info_change_data = True
          server_API.f.write( info )
          server_API.is_read_info_change_data = False
          logging.info( 'Записана строка [%s] в файл [%s]'%( info, server_API.filename ) )
        if server_API.read_info_translate_data == True:
          server_API.buf.append( info )


if __name__ == '__main__':
  logging.info( 'Старт программы orange_server.' )
  logging.info( 'Запуск потока обработки API' )
  server_thread = threading.Thread( target = server, args = '' )
  server_thread.start()
  logging.info( 'Запуск считывания кодов' )
  read_info()
  logging.info( "Ожидание остановки сервера API" )
  server_API.server_run = False
  while server_API.is_server_runs == True:
    pass
  logging.info( 'Сервер API остановленю ' )
  logging.info( 'Сервер API остановлен. Выход' )
  exit()
  
