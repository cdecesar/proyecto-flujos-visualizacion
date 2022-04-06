import random
import webbrowser
import folium
import re
import json
import pandas
import pathlib
from shapely.geometry import Polygon, Point, LineString
from funciones import obtener_poligono, obtener_datos_poligono, create_popup_info, auto_open
FILES_PATH = str(pathlib.Path(__file__).parent.resolve())

sectores = []
codigo_mapa = ''
while True:
    sector = input('Introduzca el sector a analizar: ')
    if sector != 'Ya':
        sectores.append(sector)
        codigo_mapa += sector + '-'
    else:
        codigo_mapa = codigo_mapa[:-1]
        break
print(codigo_mapa)
path_poligono = FILES_PATH + '\\Archivos\\poligonos_sectores_2D_2.0.csv'
fichero_poligonos = pandas.read_csv(path_poligono, delimiter=';')
datos_poligonos = fichero_poligonos['PolygonToString']

codigos_sectores = {'LECMPAU': 'Pamplona', 'LECMCJI': 'Castejon', 'LECMCJL': 'Castejon', 'LECMCJU': 'Castejon', 'LECMTLI': 'Toledo', 'LECMTLU': 'Toledo',
                    'LECMDGU': 'Domingo', 'GCCCRNE': 'Canarias', 'LECMTZI': 'Zaragoza', 'LECMTZU': 'Zaragoza', 'LECBP2R': 'Barcelona_p2r'}

MAPA = 'https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYmVsc2FyIiwiYSI6ImNsMWtnd3UyaTAwZGkzYm8zeng1ZHF6YXIifQ.zjyS9oluZL2c0sCP4krWFw'
colores = ['green', 'blue', 'red', 'yellow', 'black']

mapa = folium.Map(location=[42.41632777950267, -2.0189176134722495], tiles= None, zoom_start=8)
tile_layer = folium.TileLayer(
    tiles=MAPA,
    attr='mapbox',
    zoom_start=8,
    name=codigo_mapa,
    control=True,
    opacity=0.7
)
tile_layer.add_to(mapa)

for j in sectores:

    coordenadas_poligono_raw = re.split(",", datos_poligonos[obtener_datos_poligono(fichero_poligonos, j)])
    lista_coordenadas = obtener_poligono(coordenadas_poligono_raw)

    with open(FILES_PATH + '\\Carpeta_JSON\\Clusterizados2_' + j + '.json', "r") as f6:
        json_flujos = json.load(f6)
    f6.close()

    with open(FILES_PATH + '\\JSON_Cargados\\' + codigos_sectores.get(j) +'\\Asociacion2_' + j + '.json', "r") as f6:
        json_aeronaves = json.load(f6)
    f6.close()

    grupo_leyenda = folium.FeatureGroup('Sector: ' + str(j))

    folium.Polygon(lista_coordenadas,
                   color= 'white',
                   weight=2,
                   fill=True,
                   #fill_color="white",
                   fill_opacity=0.4).add_to(grupo_leyenda)

    for i in json_flujos:
        datos = json_flujos.get(i)
        aeronaves = json_aeronaves.get(i)

        iframe = folium.IFrame(create_popup_info(datos, i, aeronaves), height=300)
        popup = folium.Popup(iframe, min_width=700, max_width=700)

        folium.PolyLine([(datos[0][0][1], datos[0][0][0]), (datos[0][1][1], datos[0][1][0])],
                        color=random.choice(colores), weight=random.randint(1, 4),
                        tooltip='Flujo: ' + str(i), popup=popup).add_to(grupo_leyenda)

    grupo_leyenda.add_to(mapa)

folium.LayerControl().add_to(mapa)

auto_open(codigo_mapa, mapa)
