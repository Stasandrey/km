#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import logging

DEBUG_API = False
DEBUG_NET_IO = False
# Декоратор для логов 
def log( f ):
  def new_func( *args, **kwargs ):
    if DEBUG_API == True:
      logging.info( "Вызов #%s#( #%s#, #%s# )"%( f.__name__, args, kwargs) )
    r = f( *args, **kwargs )
    if DEBUG_API == True:
      logging.info( "Возврат:#%s#"%( r ) )
    return( r )
  return new_func
# Кодирование/декодирование объекта в json->строка байтов
def encode( p ):
  res = json.dumps( p ).encode( 'utf-8' )
  return res

# Возвращает раскодированный объект после приемки из сокета
def decode( p ):
  res = json.loads( p.decode( 'utf-8' ) )
  return res
