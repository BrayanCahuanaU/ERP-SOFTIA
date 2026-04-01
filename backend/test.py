from CSql import CSql

db = CSql()

if db.omConnect():
    print("✅ Conectado")

    cursor = db.omExecRS("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")

    row = db.fetch(cursor)
    while row:
        print(row)
        row = db.fetch(cursor)

else:
    print("❌ Error:", db.pcError)