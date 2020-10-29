#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
import scanner_window
import client_API
import os.path
import logging
import time
import threading
import znak_api 
#import json

class Scanner_Window( QtWidgets.QWidget, scanner_window.Ui_Scanner_Window ):
    def __init__( self,  parent = None ):
        QtWidgets.QWidget.__init__( self, parent )
        self.setupUi( self )
        self.loadCfg( "scanner.cfg" )
        self.pushConnect.clicked.connect( self.btnConnect )
        self.pushDisconnect.clicked.connect( self.btnDisconnect )
        self.pushOn.clicked.connect( self.btnOn )
        self.pushOff.clicked.connect( self.btnOff )
        self.pushClear.clicked.connect( self.btnClear )
        self.pushMakeCurrent.clicked.connect( self.btnMakeCurrent )
        self.pushCreate.clicked.connect( self.btnCreate )
        self.listSessions.itemActivated.connect( self.getSession )
        
        self.num = 0
        self.scan_running = False
    
    def loadCfg( self, filename ): 
        if os.path.exists( filename ):
            pass
        else:
            pass
    
    def readSessions( self ):
        self.listSessions.clear()
        self.listCurrent.clear()
        res = client_API.get_filelist( self.address, self.token )
        self.listSessions.addItems( res['data'] )
        res = client_API.get_current( self.address,  self.token )
        self.labelCurrent.setText( "Текущая сессия:%s"%( res['data'] ) )
    
    def enableButtons( self ):
        self.pushConnect.setEnabled( False )
        self.pushDisconnect.setEnabled( True )
        self.pushOn.setEnabled( True )
        self.pushDownload.setEnabled( True )
        self.pushRemove.setEnabled( True )
        self.pushCreate.setEnabled( True )
        self.pushMakeCurrent.setEnabled( True )
       
    def disableButtons( self ): 
        self.pushConnect.setEnabled( True )
        self.pushDisconnect.setEnabled( False )
        self.pushOn.setEnabled( False )
        self.pushOff.setEnabled( False )
        self.pushDownload.setEnabled( False )
        self.pushRemove.setEnabled( True )
        self.pushCreate.setEnabled( False )
        self.pushMakeCurrent.setEnabled( False )
    
    def btnConnect( self ):
        print( self.lineAddress.text() )
        if self.lineAddress.text() != "":
            if self.linePort.text() != "":
                if self.linePassword.text() != "":
                    self.address = self.lineAddress.text()
                    res = client_API.login( self.address, self.linePassword.text() )
                    print( res )
                    if res['result'] == 'ERROR':
                        logging.info( "Ошибка получения токена" )
                        self.labelStatus.setText( "Статус:ошибка подключения" )
                    else:
                        self.token = res['data']['token']  
                        self.labelStatus.setText( "Статус:подключен" )
                        self.listCodes.clear()
                        self.listCurrent.clear()
                        self.enableButtons()
                        self.readSessions()
                        
    def btnDisconnect( self ):
        client_API.logout( self.address, self.token )
        self.labelStatus.setText( "Статус:отключен" )
        self.disableButtons()
        self.scanning_run = False
        time.sleep( self.spinTime.value() * 3 )
        
    def btnOn( self ):
        res = client_API.set_translate( self.address, self.token, 'ON' )
        if res['result'] == 'OK':
            self.scanning_run = True
            self.pushOn.setEnabled( False )
            self.pushOff.setEnabled( True )
            self.labelOn.setText( "Онлайн режим:ON" )
            self.api = znak_api.Api()
            print( self.api.do( 'get_question', {'filename':'out.txt' }) )
            print( self.api.do( 'certification', { 'input':'out.txt', 'output':'ecp.txt' } ) )
            print( self.api.do( 'get_token', {'filename':'ecp.txt'} ) )
            
            self.server_thread = threading.Thread( target = self.scan, args = '' )
            self.server_thread.start()
                
    def scan( self ):
        while self.scanning_run == True:
            res = client_API.get_barcode( self.address, self.token )    
            while res['result'] == 'OK':
                
                sec = res['data']
                s = ''
                for i in sec:
                    if i == '"':
                        s = s + "'"
                    elif i == "'":
                        s = s + '"'
                    else:
                        s = s + i
                
                
                
                t = self.api.do( 'get_info', {'cis':s}  )['data']
    #print( res['status'] )
    #print( res['emissionType'] )
                print( t )
                s = res['data'] 
                if 'status' in t:
                   if 'emissionType' in t:
                        if t['status'] == 'APPLIED':
                            s = s + ' ТД Гарсинг '
                        else :
                            s = s + ' ---------- '
                        if t['emissionType'] == 'LOCAL':
                            s = s + ' ДС '
                        elif t['emissionType'] == 'FOREIGN':
                            s = s + ' НС '
                        else:
                            s = s + ' -- '
                           
                else:
                    s = s + ' ----------  --'
                self.listCodes.addItem( s )
                res = client_API.get_barcode( self.address, self.token )
                self.num = self.num + 1
            self.labelNum.setText( 'Всего:%s'%( str( self.num ) ) )
            time.sleep( self.spinTime.value()  )
    
    def btnOff( self ):
        self.scanning_run = False
        self.pushOn.setEnabled( True )
        self.pushOff.setEnabled( False ) 
        self.labelOn.setText( "Онлайн режим:OFF" )
    def btnClear( self ):
        self.listCodes.clear()

    def getSession( self, item ):
        self.listCurrent.clear()
        res = client_API.get_file( self.address, self.token, item.text() )
        data = []
        for item in res['data']:
            data.append( item[0:len( item ) - 1] )
        self.listCurrent.addItems( data )
        
    def btnCreate( self ):
        s, ok = QtWidgets.QInputDialog.getText( self, "Создание новой сессии", "Введите имя сессии:" )
        if ok :
            filename = s + '.cod'
            client_API.change_filename( self.address, self.token, filename )
            self.readSessions()
    def btnMakeCurrent( self ):
        print( self.listSessions.currentItem().text() )
        filename = self.listSessions.currentItem().text()
        client_API.change_filename( self.address, self.token, filename )
        self.readSessions()
            
if __name__ == "__main__":
    import sys
    logging.basicConfig( level = logging.INFO )
    app = QtWidgets.QApplication( sys.argv )
    window = Scanner_Window(  )
    window.show()
    sys.exit( app.exec_() )
