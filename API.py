#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import requests
cmd = { "connect":"auth/", 
        "disconnect":"logout/",  

        "sections":"catalogs/"
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

if __name__ == "__main__":
  addr = "api.datamark.by"
  name = "sestra74@mail.ru"
  psk = "ses123"
  logging.basicConfig( level = logging.INFO )
  logging.info( 'Запускаем в тестовом режиме.' )                                        
  id = EZ( addr, name, psk )
  id.connect()
  
  id.getProductSection()
  
  id.disconnect()







