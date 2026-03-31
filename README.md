# Módulo de Gestión de Tesis de un Sistema ERP

Estudiante abre Tes1010
    → Selecciona carrera (sessionStorage)
    → Backend valida en A01MEST y A03DEST
    → Agrega egresados (máximo 2)
    → Completa línea, título y PDF
    → Se graba en A03MTES + A03DEST

Administrativo abre Tes1200
    → Ve lista de tesis en estado 'A'
    → Selecciona una tesis
    → Elige dictaminadores
    → Se graba en A03DDOC

Para ejecutar el proyecto
- Frontend: 

*npm install*
*npm run dev*

- Backend:

*python3 -m venv venv*
*source venv/bin/activate*
*pip install fastapi uvicorn*
*pip install psycopg2-binary*
*uvicorn main:app --reload*

Para restaurar la base de datos en psql (SQL Shell):

*CREATE DATABASE DBERP;*
*pg_restore -U postgres -d DBERP "C:\Users\Romero\Downloads\DBERP.backup"*

Verificar que se restauró:
*psql -U postgres -d DBERP*



#Usuario para probar

Estudiante:
    Usuario: 60793117
    Contra: *                               

Administrativo:
    Usuario: 1221
    Contra: *                               