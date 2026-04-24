#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import json
import time
import random
import re
import datetime
from CBase import *
from CSql import *

class CTesis():

   def __init__(self):
       self.paData  = []
       self.paDatos = []
       self.laData  = []
       self.laDatos = []
       self.loSql   = CSql()

   def mxValParamCodigoUsuario(self):
       if not 'CCODUSU' in self.paData or not re.match('^[0-9A-Z\-]{4}$', self.paData['CCODUSU']):
          self.pcError = 'CÓDIGO DE USUARIO NO DEFINIDO O INVÁLIDO'
          return False
       return True   

   def mxValParamDNI(self):
       if not 'CNRODNI' in self.paData or not re.match('^[0-9A-Z\-]{8}$', self.paData['CNRODNI']):
          self.pcError = 'DOCUMENTO DE IDENTIDAD NO DEFINIDO O INVÁLIDO'
          return False
       return True   

   def mxValParamCodigoEstudiante(self):
       if not 'CCODEST' in self.paData or not re.match('^[0-9A-Z\-]{6}$', self.paData['CCODEST']):
          self.pcError = 'CÓDIGO DE ESTUDIANTE NO DEFINIDO O INVÁLIDO'
          return False
       return True

   def mxValParamUnidadAcademica(self):
       if not 'CUNIACA' in self.paData or not re.match('^[0-9A-Z\-]{4}$', self.paData['CUNIACA']):
          self.pcError = 'UNIDAD ACADÉMICA NO DEFINIDA O INVÁLIDA'
          return False
       return True

   def mxValParamIdTesis(self):
       if not 'CIDTESI' in self.paData or not re.match('^[0-9A-Z\-]{4}$', self.paData['CIDTESI']):
          self.pcError = 'ID TESIS NO DEFINIDO O INVÁLIDO'
          return False
       return True

   def mxVerPermisos(self):
       return True

   # -------------------------------------------------------------------------
   # Cargar carreras disponibles (para pantalla 1 de TES1010)
   # -------------------------------------------------------------------------
   def omCargarCarreras(self):
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False

       laDatos = []
       lcSql = """SELECT DISTINCT B.cUniAca, B.cNomUni 
                  FROM A02MLIN A 
                  INNER JOIN A01MUAC B ON B.cUniAca = A.cUniAca 
                  WHERE A.cEstado = 'A' 
                  ORDER BY B.cNomUni"""
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       while laTmp != None:
          laDatos.append({'CUNIACA': laTmp[0], 'CNOMUNI': laTmp[1]})
          laTmp = self.loSql.fetch(RS)

       if len(laDatos) == 0:
          self.pcError = "NO HAY CARRERAS CON LÍNEAS DE INVESTIGACIÓN DISPONIBLES"
          self.loSql.omDisconnect()
          return False

       # Obtener carrera asignada del estudiante
       lcUniAcaEstudiante = None
       if 'CCODEST' in self.paData and self.paData['CCODEST']:
           lcSql = f"SELECT cUniAca FROM A01MEST WHERE cCodEst = '{self.paData['CCODEST']}'"
           RS = self.loSql.omExecRS(lcSql)
           laTmp = self.loSql.fetch(RS)
           if laTmp:
               lcUniAcaEstudiante = laTmp[0]

       self.loSql.omDisconnect()
       self.paData = {
           'DATOS': laDatos,
           'CUNIACA_ESTUDIANTE': lcUniAcaEstudiante
       }
       return True

   # -------------------------------------------------------------------------
   # Cargar tesis del estudiante (TES1100)
   # -------------------------------------------------------------------------
   def omCargarTesisEstudiante(self):
       llOk = self.mxValParamCodigoEstudiante()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False

       laDatos = []
       lcSql = f"""SELECT A.cIdTesi, A.cLinea, A.mTitulo, B.cCodEst, B.mBitaco,
                          C.cNomUni, D.cDescri
                   FROM A03MTES A
                   INNER JOIN A03DEST B ON B.cIdTesi = A.cIdTesi
                   INNER JOIN A01MUAC C ON C.cUniAca = (SELECT cUniAca FROM A01MEST WHERE cCodEst = B.cCodEst)
                   LEFT JOIN A02MLIN D ON D.cLinea = A.cLinea
                   WHERE B.cCodEst = '{self.paData['CCODEST']}'
                   ORDER BY A.cIdTesi DESC"""
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       while laTmp != None:
          laDatos.append({
              'CIDTESI': laTmp[0],
              'CLINEA':  laTmp[1],
              'MTITULO': laTmp[2],
              'CCODEST': laTmp[3],
              'CNOMUNI': laTmp[5],
              'CDESCRI': laTmp[6]
          })
          laTmp = self.loSql.fetch(RS)

       self.loSql.omDisconnect()
       self.paData = {'DATOS': laDatos}
       return True

   # -------------------------------------------------------------------------
   # Inicio presentar PDT
   # 2026-03-23 FPM Creacion
   # -------------------------------------------------------------------------
   def omInitPresentarPDT(self):
       llOk = self.mxValParamCodigoEstudiante()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxInitPresentarPDT()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxCargarLineas()
       self.loSql.omDisconnect()
       return llOk

   def mxInitPresentarPDT(self):
       # Carga unidad academica + fecha de egreso
       lcSql = f"""SELECT A.cUniAca, B.cNomUni, A.dEgreso FROM A01MEST A 
                   INNER JOIN A01MUAC B ON B.cUniAca = A.cUniAca
                   WHERE A.cCodEst = '{self.paData['CCODEST']}'"""
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0:
          self.pcError = f"CÓDIGO DE ESTUDIANTE [{self.paData['CCODEST']}] NO EXISTE"
          return False
       elif laTmp[2] == None:
          self.pcError = f"CÓDIGO DE ESTUDIANTE [{self.paData['CCODEST']}] NO TIENE FECHA DE EGRESO"
          return False
       self.laData = {'CUNIACA': laTmp[0], 'CNOMUNI': laTmp[1], 'DATOS': None}
       # Verifica tesis
       lcSql = f"SELECT cEstado FROM A03DEST WHERE cCodEst = '{self.paData['CCODEST']}'"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0:
          pass
       elif laTmp[0] == 'X':
          pass 
       else:      
          self.pcError = f"ESTUDIANTE [{self.paData['CCODEST']}] TIENE TESIS PENDIENTE"
          return False
       return True

   def mxCargarLineas(self):
       # Carga lineas de tesis
       laDatos = []
       lcSql = f"SELECT cLinea, cDescri FROM A02MLIN WHERE cUniAca = '{self.laData['CUNIACA']}' AND cEstado = 'A' ORDER BY cLinea"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       while laTmp != None:
          laDatos.append({'CLINEA': laTmp[0], 'CDESCRI': laTmp[1]})
          laTmp = self.loSql.fetch(RS)
       if len(laDatos)== 0:
          self.pcError = f"NO HAY LÍNEAS DE INVESTIGACIÓN DE TESIS DEFINIDAS PARA UNIDAD ACADÉMICA [{self.laData['CUNIACA']}]"
          return False
       self.laData['DATOS'] = laDatos
       self.paData = self.laData 
       return True

   # -------------------------------------------------------------------------
   # Buscar egresado (en caso haya mas de un integrante por tesis)
   # 2026-03-23 FPM Creacion
   # -------------------------------------------------------------------------
   def omBuscarEgresadoTesis(self):
       llOk = self.mxValParamBuscarEgresadoTesis()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxBuscarEgresadoTesis()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamBuscarEgresadoTesis(self):
       if not self.mxValParamDNI():
          return False
       elif not self.mxValParamUnidadAcademica():
          return False
       return True   

   def mxBuscarEgresadoTesis(self):
       # Busca egresado 
       lcSql = f"""SELECT A.cCodEst, B.cName, A.dEgreso FROM A01MEST A
                   INNER JOIN S01MPER B ON B.cNroDni = A.cNroDni 
                   WHERE A.cNroDni = '{self.paData['CNRODNI']}' AND A.cUniAca = '{self.paData['CUNIACA']}'"""
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0:
          self.pcError = f"DOCUMENTO [{self.paData['CNRODNI']}] NO TIENE CÓDIGO ASIGNADO A UNIDAD ACADÉMICA DEFINIDA"
          return False
       elif laTmp[2] == None:
          self.pcError = f"CÓDIGO [{laTmp[0]}] NO TIENE FECHA DEFINIDA DE EGRESO"
          return False
       laData = {'CNRODNI': self.paData['CNRODNI'], 'CCODEST': laTmp[0], 'CNOMBRE': laTmp[1]}
       # Verifica tesis
       lcSql = f"SELECT cEstado FROM A03DEST WHERE cCodEst = '{laData['CCODEST']}'"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0:
          pass
       elif laTmp[0] == 'X':
          pass 
       else:      
          self.pcError = f"ESTUDIANTE TIENE TESIS PENDIENTE"
          return False
       self.paData = laData   
       return True

   # -------------------------------------------------------------------------
   # Grabar PDT
   # 2026-03-23 FPM Creacion
   # -------------------------------------------------------------------------
   def omGrabarPDT(self):
       llOk = self.mxValParamGrabarPDT()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxVerDatos()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxGrabarPDT()
       if llOk:
          self.loSql.omCommit()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamGrabarPDT(self):
       if not 'CLINEA' in self.paData or not re.match('^[0-9A-Z]{4}$', self.paData['CLINEA']):
          self.pcError = 'LÍNEA DE INVESTIGACIÓN DE TESIS NO DEFINIDA O INVÁLIDA'
          return False
       elif not 'CUNIACA' in self.paData or not re.match('^[0-9A-Z]{4}$', self.paData['CUNIACA']):
          self.pcError = 'UNIDAD ACADÉMICA NO DEFINIDA O INVÁLIDA'
          return False
       elif not 'MTITULO' in self.paData or not re.match('^[0-9A-ZÁÉÍÓÚÑ,.;: \-]{20,500}$', self.paData['MTITULO']):
          self.pcError = 'TÍTULO DE TESIS NO DEFINIDO O INVALIDO'
          return False
       i = 0
       for lcCodEst in self.paData['ACODEST']:
           i += 1
           if not re.match('^[0-9A-Z]{6}$', lcCodEst):
              self.pcError = f"CÓDIGO [{lcCodEst}] INVÁLIDO"
              return False
       if i == 0:
          self.pcError = f"NO HAY DATOS DE EGRESADOS"
          return False
       elif i > 2:
          self.pcError = f"HAY MÁS DE DOS EGRESADOS"
          return False
       return True

   def mxVerDatos(self):
       laData = self.paData
       for lcCodEst in self.paData['ACODEST']:
           self.paData['CCODEST'] = lcCodEst
           llOk = self.mxInitPresentarPDT()
           if not llOk:
              return False
           elif self.paData['CUNIACA'] != laData['CUNIACA']:
              self.pcError = f"UNIDAD ACADÉMICA NO CORRESPONDE PARA CÓDIGO [{lcCodEst}]"
              return False
       self.paData = laData
       # Valida unidad academica
       lcSql = f"SELECT cUniAca, cEstado FROM A02MLIN WHERE cLinea = '{self.paData['CLINEA']}'"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0:
          self.pcError = f"LÍNEA DE INVESTIGACIÓN [{self.paData['CLINEA']}] NO EXISTE"
          return False
       elif laTmp[1] != 'A':
          self.pcError = f"LÍNEA DE INVESTIGACIÓN NO ESTÁ ACTIVA"
          return False
       elif laTmp[0] != self.paData['CUNIACA']:
          self.pcError = f"UNIDAD ACADÉMICA DE LÍNEA DE INVESTIGACIÓN NO CORRESPONDE"
          return False
       return True

   def mxGrabarPDT(self):
       # Graba tesis
       lcSql = f"SELECT MAX(cIdTesi) FROM A03MTES"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp) == 0 or laTmp[0] == None:
          lcIdTesi = '0000'
       else:
          lcIdTesi = laTmp[0]
       lcIdTesi = fxCorrelativo(lcIdTesi)
       lmBitaco = fxBitacora([], {'CESTADO': 'A', 'CCODUSU': 'ZZZZ', 'TMODIFI': None})
       lcSql = f"""INSERT INTO A03MTES (cIdTesi, cLinea, mTitulo, mBitaco) VALUES ('{lcIdTesi}', '{self.paData['CLINEA']}',
                   '{self.paData['MTITULO']}', '{lmBitaco}')"""
       llOk = self.loSql.omExec(lcSql)
       if not llOk:
          self.pcError = 'NO SE PUDO INSERTAR PLAN DE TESIS'
          return False
       for lcCodEst in self.paData['ACODEST']:
           lcSql = f"INSERT INTO A03DEST (cIdTesi, cCodEst, mBitaco) VALUES ('{lcIdTesi}', '{lcCodEst}', '{lmBitaco}')"
           llOk = self.loSql.omExec(lcSql)
           if not llOk:
              self.pcError = 'NO SE PUDO INSERTAR PLAN DE TESIS PARA EGRESADO [{lcCodEst}]'
              return False
       self.paData = {'OK': 'OK'}
       return True

   # -------------------------------------------------------------------------
   # Init asignar dictaminadores PDT
   # 2026-03-23 FPM Creacion
   # -------------------------------------------------------------------------
   def omInitAsignarDictaminadoresPDT(self):
       llOk = self.mxValParamCodigoUsuario()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxInitAsignarDictaminadoresPDT()
       self.loSql.omDisconnect()
       return llOk

   def mxInitAsignarDictaminadoresPDT(self):
       i = 0
       lcSql = f"SELECT cUniAca, cNomUni, mCodUsu FROM A01MUAC WHERE cEstado = 'A' ORDER BY cUniAca"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       while laTmp != None:
          for laFila in laTmp[2]:
              if laFila['CTIPO'] == 'T' and laFila['CCODUSU'] == self.paData['CCODUSU']:
                 i += 1
                 llOk = self.mxCargarPendientesPDT(laTmp[0], laTmp[1])
                 if not llOk:
                    return False
          laTmp = self.loSql.fetch(RS)
       if i == 0:
          self.pcError = 'USUARIO NO TIENE PERMISOS'
          return False   
       if len(self.laDatos) == 0:
          self.pcError = f"NO HAY PLANES DE TESIS PENDIENTES"
          return False
       #self.paDatos = self.laDatos.sort(key=lambda k: k['TPRESEN'])
       self.paDatos = sorted(self.laDatos, key=lambda k: k['TPRESEN'])
       return True
       
   def mxCargarPendientesPDT(self, p_cUniAca, p_cNomUni):
       # Carga PDTs
       lcSql = f"""SELECT A.cIdTesi, TO_CHAR(A.tPresen, 'YYYY-MM-DD HH24:MI'), A.mTitulo, A.cLinea, B.cDescri 
                   FROM A03MTES A
                   INNER JOIN A02MLIN B ON B.cLinea = A.cLinea 
                   WHERE A.cEstado = 'A' AND B.cUniAca = '{p_cUniAca}'
                   ORDER BY A.tPresen"""
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       while laTmp != None:
          laData = {'CIDTESI': laTmp[0], 'TPRESEN': laTmp[1], 'MTITULO': laTmp[2], 'CLINEA': laTmp[3], 'CDESLIN': laTmp[4], 'CNOMEST': None, 'NFLAG': 0, 'CNOMUNI': p_cNomUni}
          llFirst = True
          i = 0
          lcSql = f"""SELECT C.cName FROM A03DEST A 
                      INNER JOIN A01MEST B ON B.cCodEst = A.cCodEst
                      INNER JOIN S01MPER C ON C.cNroDni = B.cNroDni
                      WHERE A.cIdTesi = '{laTmp[0]}' ORDER BY C.cName"""
          R1 = self.loSql.omExecRS(lcSql)
          laTmp1 = self.loSql.fetch(R1)
          while laTmp1 != None:
             i += 1
             if llFirst:
                llFirst = False
                laData['CNOMEST'] = laTmp1[0]
             laTmp1 = self.loSql.fetch(R1)
          if i == 0:
             self.pcError = f"ID DE TESIS [{laTmp[0]}] NO TIENE EGRESADOS ASIGNADOS"
             return False
          laData['NFLAG'] = i   
          self.laDatos.append(laData)
          laTmp = self.loSql.fetch(RS)
       return True

   # -------------------------------------------------------------------------
   # Cargar dictaminadores de PDT
   # 2026-03-22 FPM Creacion
   # -------------------------------------------------------------------------
   def omCargarDictaminadoresPDT(self):
       llOk = self.mxValParamIdTesis()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxVerDictaminadoresPDT()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxCargarDictaminadoresPDT()
       self.loSql.omDisconnect()
       return llOk

   def mxVerDictaminadoresPDT(self):
       lcSql = f"SELECT cEstado, mBitaco FROM A03MTES WHERE cIdTesi = '{self.paData['CIDTESI']}'"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0:
          self.pcError = f"ID TESIS NO EXISTE"
          return False
       elif laTmp[0] != 'A':
          self.pcError = f"ESTADO DE TESIS NO PERMITE ASIGNAR DICTAMINADORES DE PLAN DE TESIS"
          return False
       self.laData = {'MBITACO': laTmp[1]}
       lcSql = f"SELECT cCodDoc FROM A03DDOC WHERE cIdTesi = '{self.paData['CIDTESI']}' AND cTipo = 'P' AND cEstado = 'A'"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not (not laTmp or len(laTmp)== 0):
          self.pcError = f"TESIS YA TIENE DEFINIDOS DICTAMINADORES DE PLAN DE TESIS"
          return False
       return True

   def mxCargarDictaminadoresPDT(self):
       # Carga docentes
       laCodDoc = []
       laDatos = []
       lcSql = f"SELECT cCodDoc, cNombre FROM F_A02DDOC_1('{self.paData['CIDTESI']}')"
       #print(lcSql)           
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       while laTmp != None:
          laCodDoc.append({'CCODDOC': laTmp[0], 'CNOMBRE': laTmp[1]})
          laTmp = self.loSql.fetch(RS)
       if len(laCodDoc) < 2:
          self.pcError = "NO HAY DOCENTES SUFICIENTES PARA NOMBRAR DICTAMINADORES DE PLAN DE TESIS"
          return False
       elif len(laCodDoc)== 2:
          for laTmp in laCodDoc:
              laDatos.append({'CCODDOC': laTmp['CCODDOC'], 'CNOMBRE': laTmp['CNOMBRE']})
       else:
          llFlag = False
          i = 0
          while True:
             for laTmp in laCodDoc:
                 if random.random() <= 0.8:
                    if not laTmp['CCODDOC'] in laCodDoc:
                       laDatos.append({'CCODDOC': laTmp['CCODDOC'], 'CNOMBRE': laTmp['CNOMBRE']})
                       i += 1
                       if i == 2:
                          llFlag = True
                          break
             if llFlag:
                break             
       laDatos = sorted(laDatos, key=lambda k: (k["CNOMBRE"]))
       self.paDatos = laDatos
       return True
       
   # -------------------------------------------------------------------------
   # Grabar dictaminadores de PDT
   # 2026-03-22 FPM Creacion
   # -------------------------------------------------------------------------
   def omGrabarDictaminadoresPDT(self):
       llOk = self.mxValParamGrabarDictaminadoresPDT()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxVerDictaminadoresPDT()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxGrabarDictaminadoresPDT()
       if llOk:
          self.loSql.omCommit()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamGrabarDictaminadoresPDT(self):
       if not self.mxValParamCodigoUsuario():
          return False
       elif not self.mxValParamIdTesis():
          return False
       i = 0
       for lcCodDoc in self.paData['DATOS']:
           #print(lcCodDoc)
           if not re.match('^[0-9A-Z]{4}$', lcCodDoc):
              self.pcError = 'CÓDIGO DE DOCENTE NO DEFINIDO O INVÁLIDO'
              return False
           i += 1
       if i != 2:
          self.pcError = 'DEBEN DEFINIRSE DOS DOCENTES COMO DICTAMINADORES'
          return False
       return True

   def mxGrabarDictaminadoresPDT(self):
       for lcCodDoc in self.paData['DATOS']:
           lcSql = f"SELECT cEstado FROM S01MUSU WHERE cCodUsu = '{lcCodDoc}' AND cTipo = 'D'"
           RS = self.loSql.omExecRS(lcSql)
           laTmp = self.loSql.fetch(RS)
           if not laTmp or len(laTmp)== 0:
              self.pcError = f"CÓDIGO DOCENTE [{lcCodDoc}] NO EXISTE"
              return False
           elif laTmp[0] != 'A':
              self.pcError = f"CÓDIGO DOCENTE [{lcCodDoc}] NO ESTÁ ACTIVO"
              return False
       lmBitaco = fxBitacora([], {'CCODUSU': self.paData['CCODUSU'], 'CESTADO': 'A', 'TMODIFI': None})
       for lcCodDoc in self.paData['DATOS']:
           lcSql = f"INSERT INTO A03DDOC (cIdTesi, cTipo, cCodDoc, mBitaco) VALUES ('{self.paData['CIDTESI']}', 'P', '{lcCodDoc}', '{lmBitaco}')"
           llOk = self.loSql.omExec(lcSql)
           if not llOk:
              print(lcSql)
              self.pcError = "NO SE PUDO INSERTAR DOCENTES DICTAMINADORES DE PLAN DE TESIS"
              return False
       print('0)', self.laData['MBITACO'])      
       lmBitaco = fxBitacora(self.laData['MBITACO'], {'CCODUSU': self.paData['CCODUSU'], 'CESTADO': 'B', 'TMODIFI': None})
       lcSql = f"UPDATE A03MTES SET cEstado = 'B', mBitaco = '{lmBitaco}' WHERE cIdTesi = '{self.paData['CIDTESI']}'"
       llOk = self.loSql.omExec(lcSql)
       if not llOk:
          print(lcSql)
          self.pcError = "NO SE PUDO ACTUALIZAR ESTADO DE TESIS PARA DOCENTES DICTAMINADORES DE PLAN DE TESIS"
          return False
       self.paData = {'OK': 'OK'}    
       return True

   # -------------------------------------------------------------------------
   # Init revisar PDT
   # 2026-03-22 FPM Creacion
   # -------------------------------------------------------------------------
   def omInitRevisarPDT(self):
       llOk = self.mxValParamInitRevisarPDT()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxInitRevisarPDT()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamInitRevisarPDT(self):
       if not self.mxValParamCodigoUsuario():
          return False
       return True

   def mxInitRevisarPDT(self):
       laDatos = []
       # Cargar las tesis en A03MTES.cEstado = 'B' que tenga su codigo de docente A03DDOC.cCodDoc = '{self.paData['CCODUSU]}' AND cEstado = 'A' AND cTipo = 'P' 
       # TODO
       if len(laDatos) == 0:
          self.pcError = f"USUARIO [{self.paData['CCODUSU']}] NO TIENE PLANES DE TESIS PENDIENTES DE REVISIÓN"
          return False
       self.paDatos = laDatos    
       return True

   # -------------------------------------------------------------------------
   # Observar PDT
   # 2026-03-22 FPM Creacion
   # -------------------------------------------------------------------------
   def omObservarPDT(self):
       llOk = self.mxValParamObservarPDT()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxVerificarPDT()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxObservarPDT()
       if llOk:
          self.loSql.omCommit()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamObservarPDT(self):
       if not self.mxValParamCodigoUsuario():
          return False
       elif not self.mxValParamIdTesis():
          return False
       # FALTA VALIDAR LA OBSERVACION MOBSERV
       return True

   def mxVerificarPDT(self):
       # Verifica que A03MTES.cEstado = 'B' y que el self.paData['CCODUSU'] este en el A03DDOC para el cIdTesi, aprovechar para cargar las observaciones anteriores
       # en self.laData['MOBSERV']
       # TODO
       return True

   def mxObservarPDT(self):
       # Juntar las observaciones con el codigo de usuario y la observacion nueva
       # TODO
       # Grabar la observacion en A03DDOC
       # TODO
       return True

   # -------------------------------------------------------------------------
   # Aprobar PDT
   # 2026-03-22 FPM Creacion
   # -------------------------------------------------------------------------
   def omAprobarPDT(self):
       llOk = self.mxValParamAprobarPDT()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxVerificarPDT()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxAprobarPDT()
       if llOk:
          self.loSql.omCommit()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamAprobarPDT(self):
       if not self.mxValParamCodigoUsuario():
          return False
       elif not self.mxValParamIdTesis():
          return False
       # FALTA VALIDAR LA OBSERVACION MOBSERV
       return True

   def mxAprobarPDT(self):
       # Actualizar la aprobacion en A03DDOC
       # TODO
       # Verificar si el otro docente aprobo, si es asi actualzar el A03MTES.cEstado = 'C'
       return True

   # -------------------------------------------------------------------------
   # Init asignar asesor de BDT
   # 2026-03-25 FPM Creacion
   # -------------------------------------------------------------------------
   def omInitAsignarAsesorBDT(self):
       llOk = self.mxValParamInitAsignarAsesorBDT()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxCargarUnidadAcademica()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxInitAsignarAsesorBDT()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamInitAsignarDictaminadoresPDT(self):
       if not self.mxValParamCodigoUsuario():
          return False
       return True

   def mxInitAsignarAsesorBDT(self):
       laDatos = []
       lcSql = f"""SELECT A.cIdTesi, TO_CHAR(A.tPresen, 'YYYY-MM-DD HH24:MI'), A.mTitulo, A.cLinea, B.cDescri FROM A03MTES A
                   INNER JOIN A02MLIN B ON B.cLinea = A.cLinea 
                   WHERE A.cEstado = 'C' AND B.cUniAca = '{self.laData['CUNIACA']}'
                   ORDER BY A.tPresen"""   # OJOFPM el orden hay que corregir
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       while laTmp != None:
          laData = {'CIDTESI': laTmp[0], 'TPRESEN': laTmp[1], 'MTITULO': laTmp[2], 'CLINEA': laTmp[3], 'CDESLIN': laTmp[4], 'CNOMEST': None, 'NFLAG': 0}
          llFirst = True
          i = 0
          lcSql = f"""SELECT C.cName FROM A03DEST A 
                      INNER JOIN A01MEST B ON B.cCodEst = A.cCodEst
                      INNER JOIN S01MPER C ON C.cNroDni = B.cNroDni
                      WHERE A.cIdTesi = '{laTmp[0]}' ORDER BY C.cName"""
          R1 = self.loSql.omExecRS(lcSql)
          laTmp1 = self.loSql.fetch(R1)
          while laTmp1 != None:
             i += 1
             if llFirst:
                llFirst = False
                laData['CNOMEST'] = laTmp1[0]
             laTmp1 = self.loSql.fetch(R1)
          if i == 0:
             self.pcError = f"ID DE TESIS [{laTmp[0]}] NO TIENE EGRESADOS ASIGNADOS"
             return False
          laData['NFLAG'] = i   
          laDatos.append(laData)
          laTmp = self.loSql.fetch(RS)
       if len(laDatos)== 0:
          self.pcError = f"NO HAY PLANES DE TESIS APROBADOS PENDIENTES"
          return False
       self.laData['DATOS'] = laDatos
       self.paData = self.laData
       return True

   # -------------------------------------------------------------------------
   # Buscar docente para asesor 
   # 2026-03-25 FPM Creacion
   # -------------------------------------------------------------------------
   def omBuscarDocente(self):
       llOk = self.mxValParamBuscarDocente()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxBuscarDocente()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamBuscarDocente(self):
       if not 'CPARAM' in self.paData or not re.match('^[0-9A-Z ]{5, 20}$', self.paData['CPARAM']):
          self.pcError = 'PARÁMETRO DE BÚSQUEDA NO DEFINIDO O INVÁLIDO'
          return False
       return True   

   def mxBuscarDocente(self):
       laDatos = []
       lcNombre = self.paData['CPARAM'].strip().replace(' ', '%') + '%'
       lcSql = f"""SELECT A.cCodUsu, B.cName FROM S01MUSU A
                   INNER JOIN S01MPER B ON B.cNroDni = A.cNroDni 
                   WHERE B.cName LIKE '{lcNombre}' ORDER BY B.cName"""   # OJOFPM el orden hay que corregir
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       while laTmp != None:
          laDatos.append({'CCODDOC': laTmp[0], 'CNOMBRE': laTmp[1]})
          laTmp = self.loSql.fetch(RS)
       if len(laDatos)== 0:
          self.pcError = f"NO HAY DOCENTES QUE CUMPLAN CRITERIO DE BÚSQUEDA"
          return False
       self.paDatos = laDatos
       return True

   # -------------------------------------------------------------------------
   # Grabar asesor de BDT
   # 2026-03-22 FPM Creacion
   # -------------------------------------------------------------------------
   def omGrabarAsesorBDT(self):
       llOk = self.mxValParamGrabarAsesorBDT()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxVerAsesorBDT()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxGrabarAsesorBDT()
       if llOk:
          self.loSql.omCommit()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamGrabarAsesorBDT(self):
       if not self.mxValParamCodigoUsuario():
          return False
       elif not self.mxValParamIdTesis():
          return False
       elif not 'CCODDOC' in self.paData or not re.match('^[0-9A-Z\-]{4}$', self.paData['CCODDOC']):
          self.pcError = 'CÓDIGO DE DOCENTE NO DEFINIDO O INVÁLIDO'
          return False
       return True

   def mxGrabarAsesorBDT(self):
       # Falta validar que cCodDoc este en S01MUSU y este vigente, ademas que el A03MTES.cEstado sea C
       # TODO
       lmBitaco = fxBitacora([], {'CCODUSU': self.paData['CCODUSU'], 'CESTADO': 'A', 'TMODIFI': None})
       lcSql = f"INSERT INTO A03DDOC (cIdTesi, cTipo, cCodDoc, mBitaco) VALUES ('{self.paData['CIDTESI']}', 'A', '{laTmp['CCODDOC']}', '{lmBitaco}')"
       llOk = self.loSql.omExec(lcSql)
       if not llOk:
          self.pcError = "NO SE PUDO INSERTAR ASESOR DE BORRADOR DE TESIS"
          return False
       lmBitaco = fxBitacora(self.laData['MBITACO'], {'CCODUSU': self.paData['CCODUSU'], 'CESTADO': 'D', 'TMODIFI': None})
       lcSql = f"UPDATE A03MTES SET cEstado = 'D', mBitaco = '{lmBitaco}' WHERE cIdTesi = '{self.paData['CIDTESI']}'"
       llOk = self.loSql.omExec(lcSql)
       if not llOk:
           self.pcError = "NO SE PUDO ACTUALIZAR ESTADO DE ASESORÍA DE TESIS"
           return False
       self.paData = {'OK': 'OK'}    
       return True