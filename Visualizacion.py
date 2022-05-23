import re
import json
import pandas
import random
import folium
import shutil
import pathlib
import webbrowser
from shapely.geometry import Polygon
from funciones import obtener_poligono, obtener_datos_poligono, create_popup_info


class Visualizacion():
    def __init__(self, sector=None):

        self.colores = ['#94c4fe', '#150be6', '#0080ff','#4d59fb']

        if isinstance(sector, str):
            self.sector = []
            self.sector.append(sector)
        elif isinstance(sector, list):
            self.sector = sector
        else:
            self.sector = []
            eleccion = input('Para estudiar un unico sector introduzca "1": \n'
                             'Para analizar varios sectores juntos introduzca "2": \n')
            if eleccion == '1':
                s = input('Introduzca el sector a analizar: ')
                self.sector.append(s)
            else:
                while True:
                    s = input('Introduzca el sector a analizar: ')
                    if s != 'Ya':
                        self.sector.append(s)
                    else:
                        break

        self.FILES_PATH = str(pathlib.Path(__file__).parent.resolve())

        if len(self.sector) == 1:
            self.cargar_info_un_mapa()
            self.mostrar(self.cargar_un_mapa())
        else:
            self.mostrar(self.cargar_varios_mapas())


    def cargar_info_un_mapa(self):
        with open(self.FILES_PATH + '\\Carpeta_JSON\\Clusterizados2_' + self.sector[0] + '.json', "r") as f6:
            self.json_flujos = json.load(f6)
        f6.close()

        with open(self.FILES_PATH + '\\Carpeta_JSON\\Asociacion2_' + self.sector[0] + '.json', "r") as f6:
            self.json_aeronaves = json.load(f6)
        f6.close()

        path_poligono = self.FILES_PATH + '\\Archivos\\poligonos_sectores_2D_2.0.csv'
        fichero_poligonos = pandas.read_csv(path_poligono, delimiter=';')
        datos_poligonos = fichero_poligonos['PolygonToString']

        coordenadas_poligono_raw = re.split(",", datos_poligonos[obtener_datos_poligono(fichero_poligonos, self.sector[0])])
        self.lista_coordenadas = obtener_poligono(coordenadas_poligono_raw)
        self.poligono1 = Polygon(self.lista_coordenadas)

        self.organizar_vuelos()

    def organizar_vuelos(self):
        self.lista_ordenada_naves = []
        for i in self.json_aeronaves:
            self.lista_ordenada_naves.append(len(self.json_aeronaves.get(i)))

        self.max = max(self.lista_ordenada_naves)

    def calcular_grosor(self, flujo):
        naves = self.json_aeronaves.get(flujo)

        ratio = len(naves)/self.max

        if ratio <= 1 and ratio >= 0.75:
            return 5
        elif ratio < 0.75 and ratio >= 0.5:
            return 4
        elif ratio < 0.5 and ratio >= 0.25:
            return 3
        else:
            return 2

    def calcular_color(self, flujo):

        grosor = self.calcular_grosor(flujo)
        if grosor == 5:
            return self.colores[0]
        elif grosor == 4:
            return self.colores[1]
        elif grosor == 3:
            return self.colores[2]
        else:
            return self.colores[3]

    def cargar_un_mapa(self):

        centro = self.poligono1.centroid
        lon = centro.bounds[1]
        lat = centro.bounds[0]

        MAPA = 'https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYmVsc2FyIiwiYSI6ImNsMWtnd3UyaTAwZGkzYm8zeng1ZHF6YXIifQ.zjyS9oluZL2c0sCP4krWFw'
        #colores = ['green', 'blue', 'red', 'yellow', 'black']
        colores = ['#0080ff', '#150be6', '#94c4fe']

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
                            color=self.calcular_color(i), weight=self.calcular_grosor(i),
                            tooltip='Flujo: ' + str(i), popup=popup).add_to(grupo_leyenda)

            grupo_leyenda.add_to(self.mapa)

        folium.LayerControl().add_to(self.mapa)
        return self.sector[0]

    def mostrar(self, nombre):
        path = '\\Mapas\\Mapa-' + nombre + '.html'
        html_page = f'{self.FILES_PATH + path}'
        self.mapa.save(html_page)
        new = 2
        webbrowser.open(html_page, new=new)

    def cargar_varios_mapas(self):

        path_poligono = self.FILES_PATH + '\\Archivos\\poligonos_sectores_2D_2.0.csv'
        fichero_poligonos = pandas.read_csv(path_poligono, delimiter=';')
        datos_poligonos = fichero_poligonos['PolygonToString']

        codigo_mapa = ''
        for s in self.sector:
            codigo_mapa += s + '-'
        codigo_mapa = codigo_mapa[:-1]

        codigos_sectores = {'LECMPAU': 'Pamplona', 'LECMCJI': 'Castejon', 'LECMCJL': 'Castejon',
                                 'LECMCJU': 'Castejon', 'LECMTLI': 'Toledo', 'LECMTLU': 'Toledo',
                                 'LECMDGU': 'Domingo', 'GCCCRNE': 'Canarias', 'LECMTZI': 'Zaragoza',
                                 'LECMTZU': 'Zaragoza', 'LECBP2R': 'Barcelona_p2r'}

        MAPA = 'https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYmVsc2FyIiwiYSI6ImNsMWtnd3UyaTAwZGkzYm8zeng1ZHF6YXIifQ.zjyS9oluZL2c0sCP4krWFw'
        colores = ['green', 'blue', 'red', 'yellow', 'black']

        self.mapa = folium.Map(location=[42.41632777950267, -2.0189176134722495], tiles=None, zoom_start=8)
        tile_layer = folium.TileLayer(
            tiles=MAPA,
            attr='mapbox',
            zoom_start=8,
            name=codigo_mapa,
            control=True,
            opacity=0.7
        )
        tile_layer.add_to(self.mapa)

        for j in self.sector:

            coordenadas_poligono_raw = re.split(",", datos_poligonos[obtener_datos_poligono(fichero_poligonos, j)])
            lista_coordenadas = obtener_poligono(coordenadas_poligono_raw)

            with open(self.FILES_PATH + '\\Carpeta_JSON\\Clusterizados2_' + j + '.json', "r") as f6:
                json_flujos = json.load(f6)
            f6.close()

            with open(self.FILES_PATH + '\\Carpeta_JSON\\Asociacion2_' + j + '.json',
                      "r") as f6:
                json_aeronaves = json.load(f6)
            f6.close()

            grupo_leyenda = folium.FeatureGroup('Sector: ' + str(j))

            folium.Polygon(lista_coordenadas,
                           color='white',
                           weight=2,
                           fill=True,
                           # fill_color="white",
                           fill_opacity=0.4).add_to(grupo_leyenda)

            for i in json_flujos:
                datos = json_flujos.get(i)
                aeronaves = json_aeronaves.get(i)

                iframe = folium.IFrame(create_popup_info(datos, i, aeronaves), height=300)
                popup = folium.Popup(iframe, min_width=700, max_width=700)

                folium.PolyLine([(datos[0][0][1], datos[0][0][0]), (datos[0][1][1], datos[0][1][0])],
                                color=self.calcular_color(i), weight=self.calcular_grosor(i),
                                tooltip='Flujo: ' + str(i), popup=popup).add_to(grupo_leyenda)

            grupo_leyenda.add_to(self.mapa)

        folium.LayerControl().add_to(self.mapa)
        return codigo_mapa

if __name__ == "__main__":
    app = Visualizacion()