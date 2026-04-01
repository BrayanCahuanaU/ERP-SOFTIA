import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from CTesis import CTesis
from CAuth import CAuth
import json

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/')
async def root(request: Request):

   content_type = request.headers.get('content-type')

   if 'multipart/form-data' in content_type:
      form = await request.form()
      laData = dict(form)

      # convertir ACODEST de string a lista
      if 'ACODEST' in laData:
         laData['ACODEST'] = json.loads(laData['ACODEST'])

      file = form.get('file')

   else:
      laData = await request.json()
      file = None

   lo = None
   print(laData)

   if laData['ID'] == 'LOGIN_ADMINISTRATIVO':
      lo = CAuth()
      lo.paData = laData
      llOk = lo.omLoginAdministrativo()
      if llOk:
         return lo.paData
      else:
         return {'ERROR': lo.pcError}

   elif laData['ID'] == 'LOGIN_ESTUDIANTE':
      lo = CAuth()
      lo.paData = laData
      llOk = lo.omLoginEstudiante()
      if llOk:
         return lo.paData
      else:
         return {'ERROR': lo.pcError}

   elif laData['ID'] == 'TES1010i':
      lo = CTesis()
      lo.paData = laData
      llOk = lo.omInitTesis()
      if llOk:
         return lo.paData
      else:
         return {'ERROR': lo.pcError}

   elif laData['ID'] == 'TES1010b':
      lo = CTesis()
      lo.paData = laData
      llOk = lo.omBuscarEgresadoTesis()
      if llOk:
         return lo.paData
      else:
         return {'ERROR': lo.pcError}

   elif laData['ID'] == 'TES1010g':
      lo = CTesis()
      lo.paData = laData
      lo.poFile = file   # NUEVO
      llOk = lo.omGrabarPlanTesis()
      if llOk:
         return lo.paData
      else:
         return {'ERROR': lo.pcError}

   elif laData['ID'] == 'TES1020i':
      lo = CTesis()
      lo.paData = laData
      llOk = lo.omInitAsignarDictaminadoresPDT()
      if llOk:
         return lo.paData
      else:
         return {'ERROR': lo.pcError}

   elif laData['ID'] == 'TES1020c':
      lo = CTesis()
      lo.paData = laData
      llOk = lo.omCargarDictaminadoresPDT()
      if llOk:
         return lo.paDatos
      else:
         return {'ERROR': lo.pcError}

   elif laData['ID'] == 'TES1020g':
      lo = CTesis()
      lo.paData = laData
      llOk = lo.omGrabarDictaminadoresPDT()
      if llOk:
         return lo.paData
      else:
         return {'ERROR': lo.pcError}

   else:
      return {'ERROR': 'ID DE PROCESO NO EXISTE (MICROSERVICIOS ERP)'}