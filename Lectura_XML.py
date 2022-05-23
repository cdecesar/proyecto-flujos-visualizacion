import json
from bs4 import BeautifulSoup

with open('XML HISTORICO.xml', 'r') as f:
    data = f.read()
f.close()

Bs_data = BeautifulSoup(data, "xml")
sweeps = Bs_data.find_all('sweep')

datos = {}
for i in sweeps:
    id = i.get('id')
    aviones = i.find_all('LFZ')
    lista = []
    for j in aviones:
        datos_unicos = {}
        datos_unicos.update({'ID': j.get('id')})
        datos_unicos.update({'CallSign': j.get('CS')})
        datos_unicos.update({'Level': j.get('LEV')})
        datos_unicos.update({'Lat': j.get('N')})
        datos_unicos.update({'Lon': j.get('E')})
        lista.append(datos_unicos)
    datos.update({id: lista})

with open('json_XML.json', 'w') as f:
    json.dump(datos, f, indent=4)
f.close()
