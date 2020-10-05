#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import random
import diff_func
import glob
import os.path

diff_func.DEBUG_API = True
diff_func.DEBUG_NET_IO = True

name = 'orange_pi'
PASSWORD = '1234'
addr = '0.0.0.0' 
tokens = []
# Должен ли сервер работать API?
server_run = True
# Работает ли сервер API
is_server_runs = False
# read_info меняет данные
is_read_info_change_data = False
# server меняет данные
is_server_change_data = False
# Должен ли read_info работать?
read_info_run = True
# read_info должен записывать данные?
read_info_write_data = True
# read_info должен передавать данные?
read_info_translate_data = False
# Имя файла текущего считывания
filename = "out.cod"
f = open( filename, 'at' )
buf = []

#*******************************************************************************
# Реализация API
#*******************************************************************************
# API меняет данные
is_API_change_data = False

def isToken( token ):
  res = -1
  for i, item in enumerate( tokens ):
    if item['token'] == token:
      res = i
      return res
  
# Обработка команд
@diff_func.log
def cmd_scan( data ):
    output = diff_func.encode( {'result':'OK', 'data':{'name':name} } )
    return output

@diff_func.log  
def cmd_login( data ):
  if data['password'] == PASSWORD:
    token = str( random.randint( 1000000, 9999998 ) )
    tokens.append( {'address':addr, 'token':token} )
    output = diff_func.encode( {'result':'OK', 'data':{'token':token}} )
  else:
    output = diff_func.encode( {'result':'ERROR', 'data':{}} )
  return output

@diff_func.log
def cmd_logout( data ):
  res = isToken( data['token'] )
  if res != -1:
    logging.info( "Удаление токена |%s@%s|"%( tokens[res]['token'], 
                                              tokens[res]['address'] ) )
    tokens.pop( res )
  output = diff_func.encode( {'result':'OK', 'data':{}} )
  return output

@diff_func.log
def cmd_change_filename( data ):
  global f
  global is_server_change_data
  global is_read_info_change_data
  global filename
  while is_read_info_change_data == True:
    pass
  is_server_change_data = True
  f.close()
  lfilename = filename
  filename = data['filename']
  f = open( filename, 'at' )
  is_server_change_data = False
  output = diff_func.encode( {'result':'OK', 'data':lfilename} )
  return output

@diff_func.log
def cmd_get_filelist( data ):
  list = glob.glob( "*.cod" )
  print( list )    
  output = diff_func.encode( { 'result':'OK', 'data':list } )
  return output
  
@diff_func.log
def cmd_getfile( data ):
  global is_server_change_data
  global is_read_info_change_data
  if os.path.exists( data['filename'] ) == True:
    while is_read_info_change_data == True:
      pass
    is_server_change_data = True
    with open( data['filename'], 'rt' ) as file:
      d = file.readlines()
      output = diff_func.encode( { 'result':'OK', 'data':d } )
    is_server_change_data = False
  else:
    output = diff_func.encode( { 'result':'ERROR', 'data':'File not exist' } )
  return output

@diff_func.log
def cmd_settranslate( data ):
  global read_info_translate_data
  if read_info_translate_data == True:
    res = { 'result':'OK', 'data':'ON' }
  else:
    res = { 'result':'OK', 'data':'OFF' }
  print( data )
  if data['flag'] == 'ON':
    read_info_translate_data = True
  else:
    read_info_translate_data = False
  return diff_func.encode( res )
  
@diff_func.log
def cmd_gettranslate( data ):
  global read_info_translate_data
  if read_info_translate_data == True:
    res = { 'result':'OK', 'data':'ON' }
  else:
    res = { 'result':'OK', 'data':'OFF' }
  return diff_func.encode( res )

@diff_func.log
def cmd_getbarcode( data ):
  if read_info_translate_data == True:
    if len( buf ) > 0:
      res = { 'result':'OK', 'data':buf.pop( 0 ) }
      
    else:
      res = { 'result':'ERROR', 'data':'Bufer is empty' }
  else:
    res = { 'result':'ERROR', 'data':'Translating is off' }
  return diff_func.encode( res )
      
@diff_func.log
def cmd_unknown( data ):
  output = diff_func.encode( {'result':'ERROR', 'data':'unknown command'} )
  return output

# Заполнение адресов вызовов API
commands = { 'scan':cmd_scan, 
             'login':cmd_login, 
             'logout':cmd_logout, 
             'change_filename':cmd_change_filename, 
             'get_filelist':cmd_get_filelist, 
             'get_file':cmd_getfile, 
             'set_translate':cmd_settranslate, 
             'get_translate':cmd_gettranslate, 
             'get_barcode':cmd_getbarcode}
#*******************************************************************************

