import re
import json
import pandas
import pathlib
import shapely
import geopy.distance
from shapely.geometry import Polygon, LineString, Point

SECTOR = input('Sector: ')
FILES_PATH = str(pathlib.Path(__file__).parent.resolve())
dimroute = pandas.read_csv('C:\\DATOS\\TRABAJO_CRIDA\\DATOS\\Flujos\\dimRouteClustered_R1I_R2I_SAN_PAU_CJI_BAS_CCC_2019.csv', delimiter=';')
csv = pandas.read_csv('C:\\DATOS\\TRABAJO_CRIDA\\Proyecto_Flujos\\Carpeta_CSV\\' + SECTOR + '_Final.csv', delimiter=',')
flujo_antiguo = csv['routeKey']
flightkey = csv['flightkey']
flujo_nuevo = csv['Flujo_Clusterizado']

#%%

with open(FILES_PATH + '\\Carpeta_JSON\\Clusterizados2_' + SECTOR + '.json', "r") as f6:
    json_flujos = json.load(f6)
f6.close()

with open(FILES_PATH + '\\Carpeta_JSON\\Asociacion2_' + SECTOR + '.json', "r") as f6:
    json_aeronaves = json.load(f6)
f6.close()

asociacion_flujos = {}

c = 0
contador = csv.index[c]
contador2 = 0

while contador2 < flightkey.size:

    avion = flightkey[contador]
    f_a = flujo_antiguo[contador]
    f_n = flujo_nuevo[contador]

    if f_n not in asociacion_flujos.keys():
        asociacion_flujos.update({f_n: []})

    asociaciones = asociacion_flujos.get(f_n)
    if f_a not in asociaciones:
        asociaciones.append(f_a)


    if (contador2 + 1) == flightkey.size:
        break
    else:
        c += 1
        contador = csv.index[c]
        contador2 += 1
#%%

for i in asociacion_flujos.keys():
    print(i)
    print(asociacion_flujos.get(i))
    print('-------------------------')

#%%

recorrido = dimroute['poligono']
id = dimroute['routeKey']
print(recorrido)
print(id)
#%%

dic = {}

for i in asociacion_flujos.keys():
    lista = asociacion_flujos.get(i)

    for j in lista:
        c = 0
        contador = dimroute.index[c]
        contador2 = 0
        while contador2 < recorrido.size:

            if id[contador] == j and j not in dic.keys():
                dic.update({j: []})
                print('daleeee')

                r = recorrido[contador]
                primero = re.split('\(', r)

                segundo = re.split(',', primero[1])
                cont = 1
                for k in segundo:
                    data = re.split(' ', k)
                    print(data, len(data))
                    if len(data) == 2:
                        if ')' not in data[1]:
                            lat = float(data[1])
                            lon = float(data[0])
                        else:
                            lon = float(data[0])
                            x = re.split('\)', data[1])
                            lat = float(x[0])
                    else:
                        if ')' not in data[2]:
                            lat = float(data[2])

                            lon = float(data[1])
                        else:
                            lon = float(data[1])
                            x = re.split('\)', data[2])
                            lat = float(x[0])
                    a = (lat, lon)
                    l = dic.get(j)
                    l.append(a)
                    dic[j] = l
            else:
                pass
            if (contador2 + 1) == flightkey.size:
                break
            else:
                c += 1
                contador = csv.index[c]
                contador2 += 1
#%%

for i in asociacion_flujos.keys():
    print(i)
    print(dic.get(i))
    print('-----------------------------------------------------------------')

#%%
d = {}

for i in asociacion_flujos.keys():
    a = asociacion_flujos.get(i)
    d.update({i: []})
    l = {}
    for j in a:
        b = dic.get(j)

        l.update({str(j): b})
    d[i] = l

for i in d.keys():
    print(d.get(i))

print(len(d.keys()))
#%%
with open(FILES_PATH + "\\" + SECTOR + "_NUEVOS.json", "w") as outfile:
    json.dump(d, outfile, indent=4)
outfile.close()