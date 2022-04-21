import random
import folium
import re
import json
import pandas
import pathlib
from shapely.geometry import Polygon
from funciones import obtener_poligono, obtener_datos_poligono, create_popup_info, auto_open


class Visualizacion():
    def __init__(self, sector):

        if isinstance(sector, str):
            self.sector = []
            self.sector.append(sector)
        elif isinstance(sector, list):
            self.sector = sector
        else:
            s = input('Introduzca el sector a analizar: ')

            self.sector = []
            self.sector.append(s)

        self.FILES_PATH = str(pathlib.Path(__file__).parent.resolve())

        self.cargar_info()
        self.cargar_un_mapa()
        self.mostrar()

    def cargar_info(self):
        if len(self.sector) == 1:
            with open(self.FILES_PATH + '\\Carpeta_JSON\\Clusterizados2_' + self.sector[0] + '.json', "r") as f6:
                self.json_flujos = json.load(f6)
            f6.close()

            with open(self.FILES_PATH + '\\JSON_Cargados\\Pamplona\\Asociacion2_' + self.sector[0] + '.json', "r") as f6:
                self.json_aeronaves = json.load(f6)
            f6.close()

            path_poligono = self.FILES_PATH + '\\Archivos\\poligonos_sectores_2D_2.0.csv'
            fichero_poligonos = pandas.read_csv(path_poligono, delimiter=';')
            datos_poligonos = fichero_poligonos['PolygonToString']

            coordenadas_poligono_raw = re.split(",", datos_poligonos[obtener_datos_poligono(fichero_poligonos, self.sector[0])])
            self.lista_coordenadas = obtener_poligono(coordenadas_poligono_raw)
            self.poligono1 = Polygon(self.lista_coordenadas)
        else:
            pass

    def cargar_un_mapa(self):

        centro = self.poligono1.centroid
        lon = centro.bounds[1]
        lat = centro.bounds[0]

        MAPA = 'https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYmVsc2FyIiwiYSI6ImNsMWtnd3UyaTAwZGkzYm8zeng1ZHF6YXIifQ.zjyS9oluZL2c0sCP4krWFw'
        colores = ['green', 'blue', 'red', 'yellow', 'black']


        self.mapa = folium.Map(location=[lat, lon], tiles= None, zoom_start=8)

        tile_layer = folium.TileLayer(
            tiles=MAPA,
            attr='mapbox',
            zoom_start=8,
            name=self.sector[0],
            control=True,
            opacity=0.7
        )

        tile_layer.add_to(self.mapa)

        folium.Polygon(self.lista_coordenadas,
                       color="black",
                       weight=2,
                       fill=True,
                       fill_color="white",
                       fill_opacity=0.4).add_to(self.mapa)

        for i in self.json_flujos:
            grupo_leyenda = folium.FeatureGroup('Flujo: ' + str(i))
            datos = self.json_flujos.get(i)
            aeronaves = self.json_aeronaves.get(i)

            iframe = folium.IFrame(create_popup_info(datos, i, aeronaves), height=300)
            popup = folium.Popup(iframe, min_width=700, max_width=700)

            folium.PolyLine([(datos[0][0][1], datos[0][0][0]), (datos[0][1][1], datos[0][1][0])],
                            color=random.choice(colores), weight=random.randint(1, 4),
                            tooltip='Flujo: ' + str(i), popup=popup).add_to(grupo_leyenda)

            grupo_leyenda.add_to(self.mapa)

        folium.LayerControl().add_to(self.mapa)

    def mostrar(self):
        auto_open(self.sector[0], self.mapa)
