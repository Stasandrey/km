#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
# Возвращает кодированный  объект для передачи по сокету
def encode( p ):
  res = json.dumps( p ).encode( 'utf-8' )
  return res
# Возвращает раскодированный объект после приемки из сокета
def decode( p ):
  res = json.loads( p.decode( 'utf-8' ) )
  return res
