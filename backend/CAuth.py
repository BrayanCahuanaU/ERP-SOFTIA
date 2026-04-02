#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import json
import re
from CBase import *
from CSql import *

class CAuth():

   def __init__(self):
       self.paData  = []
       self.pcError = None
       self.loSql   = CSql()

   def mxValParamDNI(self):
       if not 'CNRODNI' in self.paData or not re.match('^[0-9]{8}$', self.paData['CNRODNI']):
          self.pcError = 'DOCUMENTO DE IDENTIDAD NO DEFINIDO O INVÁLIDO'
          return False
       return True   

   def mxValParamUnidadAcademica(self):
       if not 'CUNIACA' in self.paData or not re.match('^[0-9A-Z\-]{4}$', self.paData['CUNIACA']):
          self.pcError = 'UNIDAD ACADÉMICA NO DEFINIDA O INVÁLIDA'
          return False
       return True

   def mxValParamCodigoUsuario(self):
       if not 'CCODUSU' in self.paData or not re.match('^[0-9A-Z\-]{4}$', self.paData['CCODUSU']):
          self.pcError = 'CÓDIGO DE USUARIO NO DEFINIDO O INVÁLIDO'
          return False
       return True   

   # -------------------------------------------------------------------------
   # Login Estudiante - Búsqueda por DNI y Unidad Académica
   # -------------------------------------------------------------------------
   def omLoginEstudiante(self):
       llOk = self.mxValParamDNI()
       if not llOk:
          return False
       if not 'CPASSWORD' in self.paData:
         self.pcError = 'CONTRASEÑA NO DEFINIDA'
         return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxLoginEstudiante()
       self.loSql.omDisconnect()
       return llOk

   def mxLoginEstudiante(self):
    lcSql = f"""
        SELECT A.ccodest, B.cnombre, B.cclave, A.cuniaca
        FROM a01mest A
        INNER JOIN s01mper B 
            ON B.cnrodni = A.cnrodni
        WHERE A.cnrodni = '{self.paData['CNRODNI']}'
          AND A.cestado = 'A'
    """

    RS = self.loSql.omExecRS(lcSql)
    laTmp = self.loSql.fetch(RS)

    # ❌ No existe
    if not laTmp:
        self.pcError = f"NO SE ENCONTRÓ REGISTRO PARA EL DNI [{self.paData['CNRODNI']}]"
        return False

    lcCodEst  = laTmp[0]
    lcNombre  = laTmp[1]
    lcClaveBD = laTmp[2]
    lcUniAca  = laTmp[3]

    # 🔐 Validar contraseña (texto plano)
    if lcClaveBD.strip() != self.paData['CPASSWORD'].strip():
        self.pcError = 'CONTRASEÑA INCORRECTA'
        return False

    # ✅ Retorno
    self.paData = {
        'CCODEST': lcCodEst,
        'CNOMBRE': lcNombre,
        'CUNIACA': lcUniAca
    }

    return True

   # -------------------------------------------------------------------------
   # Login Administrativo - Búsqueda por código de usuario
   # -------------------------------------------------------------------------
   def omLoginAdministrativo(self):
       llOk = self.mxValParamCodigoUsuario()
       if not llOk:
          return False
       if not 'CPASSWORD' in self.paData:
          self.pcError = 'CONTRASEÑA NO DEFINIDA'
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxLoginAdministrativo()
       self.loSql.omDisconnect()
       return llOk

   def mxLoginAdministrativo(self):
    lcSql = f"""
        SELECT U.ccodusu, P.cnombre, P.cclave
        FROM s01musu U
        INNER JOIN s01mper P 
            ON P.cnrodni = U.cnrodni
        WHERE U.ccodusu = '{self.paData['CCODUSU']}'
          AND U.cestado = 'A'
    """

    RS = self.loSql.omExecRS(lcSql)
    laTmp = self.loSql.fetch(RS)

    if not laTmp:
        self.pcError = f"CÓDIGO DE USUARIO [{self.paData['CCODUSU']}] NO EXISTE"
        return False

    lcCodigo  = laTmp[0]
    lcNombre  = laTmp[1]
    lcClaveBD = laTmp[2]

    # 🔐 generar hash MD5 del password ingresado
    if lcClaveBD.strip() != self.paData['CPASSWORD'].strip():
        self.pcError = 'CONTRASEÑA INCORRECTA'
        return False

    self.paData = {
        'CCODUSU': lcCodigo,
        'CNOMBRE': lcNombre
    }
    return True