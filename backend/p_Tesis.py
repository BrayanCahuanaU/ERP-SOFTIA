import hashlib
import requests, json

# Init presentacion de PDT
#laData = {'ID': 'TES1010i', 'CCODEST': '003WOQ'}
# Buscar egresado
#laData = {'ID': 'TES1010b', 'CNRODNI': '73343342', 'CUNIACA': '0049'}
# Grabar PDT
#laData = {'ID': 'TES1010g', 'CLINEA': '0001', 'CUNIACA': '0049', 'MTITULO': 'EVALUACIÓN DEL IMPACTO DE LOS FIREWALLS DE ÚLTIMA GENERACIÓN EN LA SEGURIDAD DE SISTEMAS OPERATIVOS: UN ANÁLISIS COMPARATIVO EN ENTORNOS LINUX Y WINDOWS', 'ACODEST': ['003WEP', '003WOQ']}
# Init asignar dictaminadores PDT
#laData = {'ID': 'TES1110i', 'CCODUSU': '1221'}
# Cargar dictaminadores PDT
#laData = {'ID': 'TES1110c', 'CIDTESI': '0001'}
# Grabar asignacion dictaminadores PDT
laData = {'ID': 'TES1110g', 'CIDTESI': '0001', 'CCODUSU': '1221', 'DATOS': ['1223', '1220']}

response = requests.post('http://localhost:8000/', json=laData)
laData = json.loads(response.text)
print(laData)


#curl -X POST http://localhost:3000/suma -H "Content-Type: application/json" -d '{"ID": "ID", "cusucod": "1221", "a": 7, "b": 4}'