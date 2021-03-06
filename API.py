#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import requests
cmd = { "connect":"auth/", 
        "disconnect":"logout/",  

        "sections":"catalogs/", 
        
        "order_codes":"orders/add/"
      
      }

class EZ:
  def __init__( self, host, login, password ):
    self.host = "https://%s/"%( host )
    self.login = login
    self.password = password
    self.token = ''
    logging.info( "Создание класса EZ. \nHost:[%s]\n\
login:[%s]\npassword:[%s]"%( 
                                                            self.host, 
                                                            self.login,
                                                            self.password ) )
      
  def connect( self ):
    logging.info( "Подключение к API" )
    res = requests.post( self.host + cmd["connect"], 
                  data = { 'username':self.login, 'password':self.password })
    self.token = res.json()['token']
    
  def disconnect( self ):
    logging.info( "Отключение от API" )
    res = requests.post( self.host + cmd["disconnect"], 
                  headers = { 'token':self.token })
    print( res )
#  Читает код и количество товаров в секции ОБУВЬ
  def getProductSection( self ):
    logging.info( "Получение списка разделов товаров" )
    res = requests.post( self.host + cmd["sections"], 
                  headers = { 'token':self.token }).json()                                                                                                                 

    for i in res['catalogs']:
      if i['name'] == 'Обувь':
        
        self.numGtins = i['count_items']
        self.codeSection = i['code']
        logging.info( "   Количество товаров в категории:[%s]"%( self.numGtins ) )
        logging.info( "   Код категории:[%s]"%( self.codeSection ) )
#  Возвращает список вида [GTIN, MODEL, SIZE]
  def getAllGtins( self ):
    logging.info( "Читаем все GTIN-ы" )
    ret = []
    addr = "%s%s%s/"%( self.host, cmd['sections'], self.codeSection )
    res = requests.post( addr, 
                  headers = { 'token':self.token } ).json()["items"]                                                                                                                 
    for i in res:
      
      
      s = "%s %s"%( i['gtin'], i['articul'] )
      for k in i['params']:
        if k['name'] == "Размер в штихмассовой системе":
          s = s + " %s"%( k['value'] )
          now = { 'gtin':i['gtin'], 'model':i['articul'], 'size':k['value'] }
          ret.append( now )
    return ret
#  Заказ num кодов маркировки для gtin
  def orderCodes( self, gtin, num ):
      logging.info( "Заказываем коды маркировки для GTIN:[%s] [%s] шт."%( 
                                                        gtin, num) )
      print( self.host + cmd["order_codes"] )
      res = requests.post( self.host + cmd["order_codes"], 
                                headers = { 'token':self.token }, data = { 
                                "label_type":7, "count":num, "gtin":int( gtin )
                                } ).json()
      print( res )

if __name__ == "__main__":
  addr = "api.datamark.by"
  name = "sestra74@mail.ru"
  psk = "ses123"
  logging.basicConfig( level = logging.INFO )
  logging.info( 'Запускаем в тестовом режиме.' )                                        
  id = EZ( addr, name, psk )
  id.connect()
  
#  id.getProductSection()
#  print( id.getAllGtins() )
  
  id.orderCodes( '04811790050238', 2 )
  
  id.disconnect()







