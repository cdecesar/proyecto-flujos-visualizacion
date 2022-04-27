import os, re, json, glob, pathlib, random
from tkinter import *
from Visualizacion import Visualizacion
from PIL import ImageTk, Image

FILES_PATH = str(pathlib.Path(__file__).parent.resolve())

lista_ventanas = []
global contador_ventanas
contador_ventanas = 1

class PopUp():
    def __init__(self, root, mensaje):
        self.top = Toplevel(root)

        self.top.title("MENSAJE DE AVISO")
        self.top.configure(bg='dimgray')
        self.top.wm_attributes("-topmost", True)
        self.top.resizable(width=False, height=False)

        self.only_pane = PanedWindow(self.top, orient=VERTICAL)
        self.only_pane.grid(column=0, row=0, rowspan=1, sticky=(N, W, E, S))
        self.only_pane.rowconfigure(0, weight=1)
        self.only_pane.columnconfigure(0, weight=1)

        self.frame1 = Frame(master=self.top, bg="dimgray", borderwidth=2, relief="raised")
        self.frame1.grid(row=0, column=0, sticky=(W, S, E, N))
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.columnconfigure(0, weight=1)
        self.only_pane.add(self.frame1)

        self.label = Label(self.frame1, text=mensaje, fg="aquamarine2", bg="dimgray", font="arial 10 bold", padx=30, pady=30)
        self.label.grid(row=0, column=0, sticky=(W, S, E, N))

        self.destruir()

    def destruir(self):
        self.top.after(1750, self.top.destroy)

class VentanaInformacion():
    def __init__(self, master, identificador_padre, flujo, tipo, sector):
        self.root = Toplevel(master)
        self.id_padre = identificador_padre
        self.flujo = flujo
        self.tipo = tipo
        self.sector = sector

        self.iniciar_root()
        self.construir()

    def iniciar_root(self):
        #self.root.resizable(width=False, height=False)
        self.root.wm_attributes("-topmost", True)
        self.root.title(self.flujo)
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)
        #self.root.geometry("100x500")


    def cargar_infobasica(self):
        with open(FILES_PATH + '\\Carpeta_JSON\\Clusterizados2_' + self.sector + '.json', "r") as f6:
            self.json_flujos = json.load(f6)
        f6.close()

        with open(FILES_PATH + '\\Carpeta_JSON\\Asociacion2_' + self.sector + '.json', "r") as f6:
            self.json_aeronaves = json.load(f6)
        f6.close()

    def construir(self):
        self.cargar_infobasica()

        if self.tipo == 1:
            self.root.resizable(width=False, height=False)

            self.frame_f1 = Label(self.root, text=self.flujo, font='arial 20 bold', width=30)
            self.frame_f1.grid(row=0, column=0, columnspan=2)

            datos = self.json_flujos.get(self.flujo)
            naves = self.json_aeronaves.get(self.flujo)

            punto1 = datos[0][0]
            punto2 = datos[0][1]
            levels = datos[1]

            limite = min(len(str(punto1[0])), len(str(punto1[1])), len(str(punto2[0])), len(str(punto2[1])))

            if limite > 8:
                limite = 8

            l1 = Label(self.root, text='PUNTO DE ENTRADA', font='arial 10 bold', pady=2, padx=2)
            l1.grid(row=1, column=0)

            l2 = Label(self.root, text='PUNTO DE SALIDA', font='arial 10 bold', pady=2, padx=2)
            l2.grid(row=2, column=0)

            l3 = Label(self.root, text='EVOLUCIOB NIVELES VUELO', font='arial 10 bold', pady=2, padx=2)
            l3.grid(row=3, column=0)

            l4 = Label(self.root, text='IMPACTO MEDIO', font='arial 10 bold', pady=2, padx=2)
            l4.grid(row=4, column=0)

            l5 = Label(self.root, text='NUMERO DE AERONAVES', font='arial 10 bold', pady=2, padx=2)
            l5.grid(row=5, column=0)

            l6 = Label(self.root, text='COSAS', font='arial 10 bold', pady=2, padx=2)
            l6.grid(row=6, column=0)

            l7 = Label(self.root, text=str(punto1[1])[0:limite] + """ ; """ + str(punto1[0])[0:limite], font='arial 10 bold', pady=2, padx=2)
            l7.grid(row=1, column=1)

            l8 = Label(self.root, text=str(punto2[1])[0:limite]+ """ ; """ + str(punto2[0])[0:limite], font='arial 10 bold', pady=2, padx=2)
            l8.grid(row=2, column=1)

            l9 = Label(self.root, text=levels[0] + """ ; """ + levels[1], font='arial 10 bold', pady=2, padx=2)
            l9.grid(row=3, column=1)

            l10 = Label(self.root, text=levels[0] + """ ; """ + levels[1], font='arial 10 bold', pady=2, padx=2)
            l10.grid(row=4, column=1)

            l11 = Label(self.root, text=str(len(naves)), font='arial 10 bold', pady=2, padx=2)
            l11.grid(row=5, column=1)

            l12 = Label(self.root, text='MAS COSAS', font='arial 10 bold', pady=2, padx=2)
            l12.grid(row=6, column=1)

        else:
            self.root.bind('<Configure>', self.resizer)
            self.im = Image.open(FILES_PATH + "\\Images\\barras.png")
            self.img = ImageTk.PhotoImage(self.im)
            self.w = int(self.img.width())
            self.h = int(self.img.height())

            # create label and add resize image
            self.label1 = Label(master=self.root, image=self.img)
            self.label1.image = self.img
            self.label1.pack()

    def resizer(self, e):
        bg1 = Image.open(FILES_PATH + "\\Images\\barras.png")
        resize_bg1 = bg1.resize((min(int(self.root.winfo_width()), self.w), min(int(self.root.winfo_height()), self.h)))
        # resize_bg1 = bg1.resize((e.width, e.height))

        new_bg = ImageTk.PhotoImage(resize_bg1)

        self.label1.config(image=new_bg)
        self.label1.image = new_bg

    def cerrar(self):
        contador = 0
        for v in lista_ventanas:
            if v.id == self.id_padre:
                break
            contador += 1

        self.root.destroy()

        lista_ventanas[contador].show()

class VentanaFlujos():
    def __init__(self, master, identificador, sector):
        self.root = Toplevel(master)
        self.id = identificador
        self.sector = sector

        self.iniciar_root()
        self.construir()

    def iniciar_root(self):
        self.root.resizable(width=False, height=False)
        self.root.wm_attributes("-topmost", True)
        self.root.title(self.sector)
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)

    def cargar_json(self):
        with open(FILES_PATH + '\\Carpeta_JSON\\Clusterizados2_' + self.sector + '.json', "r") as f6:
            json_flujos = json.load(f6)
        f6.close()
        return json_flujos

    def construir(self):
        self.datos_json = self.cargar_json()
        self.frame_f1 = Label(self.root, text='Flujos', font='arial 20 bold', width=30,
                              pady=50)
        self.frame_f1.grid(row=0, column=0, columnspan=2)

        limite = len(self.datos_json.keys())
        fila = 1
        columna = 0
        for f in self.datos_json.keys():

            a = random.choice([1,2])
            if a == 1:
                self.e = Button(self.root, text=f, font='arial 10 bold',
                                       padx=5, borderwidth=5,
                                       width=15)
                self.e["command"] = lambda s = f: self.informar(s)
            else:
                self.e = Label(self.root, text=f, font='arial 10 bold',
                                       padx=5, width=15)
            self.e.grid(row=fila, column=columna)

            if columna == 1:
                columna = 0
                fila += 1
            else:
                columna += 1
            limite -= 1

            if limite == 0:
                if len(self.datos_json.keys()) % 2 == 1:
                    extra = Label(self.root, text='\n\n\n\n')
                    extra.grid(row=fila + 1, column=0)
                else:
                    extra = Label(self.root, text='\n', pady=5)
                    extra.grid(row=fila, column=0)

    def informar(self, flujo):
        self.hide()
        v_infobasica = VentanaInformacion(lista_ventanas[0].root, self.id, flujo, 1, self.sector)
        v_infografica = VentanaInformacion(lista_ventanas[0].root, self.id, flujo, 2, self.sector)


    def hide(self):
        self.root.withdraw()

    def show(self):
        self.root.update()
        self.root.deiconify()

    def cerrar(self):
        self.root.destroy()
        contador = 0
        for v in lista_ventanas:
            if v.modo == 1:
                break
            contador += 1

        botones = lista_ventanas[contador].botones
        for b in botones:
            if b['text'] == self.sector:
                b["state"] = "normal"

        contador = 0
        for v in lista_ventanas:
            if v.id == self.id:
                break
            contador += 1

        lista_ventanas.pop(contador)

class VentanaConjunto():
    def __init__(self, master, identificador):
        self.root = Toplevel(master)
        self.id = identificador
        self.modo = 2
        self.sectores_analizar = []
        self.botones_eliminar = []

        self.iniciar_root()
        self.construir()

    def iniciar_root(self):
        # self.root.geometry('600x500')
        self.root.resizable(width=False, height=False)
        self.root.wm_attributes("-topmost", True)
        self.root.title("Análisis individual")
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)

        all_files = glob.glob(os.path.join(FILES_PATH + '\\Carpeta_JSON', "*.json"))
        self.sectores = []
        for f in all_files:
            if len(re.findall('Clusterizados2_', f)) == 1:
                self.sectores.append(re.split('Clusterizados2_', re.split('\.', f)[0])[-1])

    def construir(self):

        self.frame_f1 = Label(self.root, text='Indique el sector que quiere analizar', font='arial 20 bold', width=50,
                              pady=50)
        self.frame_f1.grid(row=0, column=0, columnspan=3)

        self.botones = []
        contador_filas = 1
        contador_columnas = 0
        contador_total = 0
        for sector in self.sectores:

            if contador_total == len(self.sectores) - 1 and len(self.sectores) % 3 == 1:
                self.boton = Button(self.root, text=sector, font='arial 12 bold', padx=15, pady=10, borderwidth=5,
                                    width=15)
                self.boton.grid(row=contador_filas, column=1)
                self.boton["command"] = lambda s = sector: self.apuntar(s)

            else:
                self.boton = Button(self.root, text=sector, font='arial 12 bold', padx=15, pady=10, borderwidth=5,
                                    width=15)
                self.boton.grid(row=contador_filas, column=contador_columnas)
                self.boton["command"] = lambda s = sector: self.apuntar(s)

            contador_columnas += 1
            if contador_columnas == 3:
                contador_filas += 1
                contador_columnas = 0
            contador_total += 1

        self.boton_siguiente = Button(self.root, text='SIGUIENTE', font='arial 12 bold', padx=15, pady=10, borderwidth=5,
                                        width=15)
        self.boton_siguiente.grid(row=((len(self.sectores) // 3) + 2), column=1)
        self.boton_siguiente['command'] = self.siguiente

        extra = Label(self.root, text='\n\n\n\n')
        extra.grid(row=((len(self.sectores) // 3) + 3), column=0)

    def apuntar(self, sector):

        if sector not in self.sectores_analizar:
            columna = 0
            fila = (len(self.sectores) // 3) + 4

            if len(self.sectores_analizar) > 0:
                columna = len(self.sectores_analizar) % 3
                fila += len(self.sectores_analizar) // 3

            self.sectores_analizar.append(sector)
            self.boton_e = Button(self.root, text='BORRAR ' + sector, font='arial 12 bold', padx=15, pady=10, borderwidth=5,
                                width=15)
            self.boton_e.grid(row=fila, column=columna)
            self.boton_e["command"] = lambda s=sector: self.borrar(s)
            self.botones_eliminar.append(self.boton_e)
        else:
            ventana_aviso = PopUp(lista_ventanas[0].root, 'EL SECTOR YA HA SIDO AÑADIDO')

    def borrar(self, sector):
        indice = self.sectores_analizar.index(sector)
        self.sectores_analizar.pop(indice)
        b = self.botones_eliminar.pop(indice)
        b.destroy()

        contador = 0
        for i in self.botones_eliminar:
            columna = contador % 3
            fila = (len(self.sectores) // 3) + 4 + contador // 3

            i.grid(row=fila, column=columna)
            contador += 1

    def siguiente(self):
        if len(self.sectores_analizar) > 0:
            self.mapa_sector = Visualizacion(self.sectores_analizar)

            self.sectores_analizar.clear()
            for b in self.botones_eliminar:
                b.destroy()
            self.botones_eliminar.clear()

            lista_ventanas[0].root.wm_attributes("-topmost", False)
            self.root.wm_attributes("-topmost", False)
            self.root.update()
            lista_ventanas[0].root.update()
        else:
            ventana_aviso = PopUp(lista_ventanas[0].root, 'DEBE SELECCIONAR AL MENOS 1 SECTOR')


    def hide(self):
        self.root.withdraw()

    def show(self):
        self.root.update()
        self.root.deiconify()


    def cerrar(self):
        self.root.destroy()
        contador = 0
        for v in lista_ventanas:
            if v.id == self.id:
                break
            contador += 1
        lista_ventanas.pop(contador)
        lista_ventanas[0].boton2["state"] = "normal"

class VentanaIndividual():
    def __init__(self, master, identificador):
        self.root = Toplevel(master)
        self.id = identificador
        self.modo = 1

        self.iniciar_root()
        self.construir()

    def iniciar_root(self):
        self.root.resizable(width=False, height=False)
        self.root.wm_attributes("-topmost", True)
        self.root.title("Análisis individual")
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)

        all_files = glob.glob(os.path.join(FILES_PATH + '\\Carpeta_JSON', "*.json"))
        self.sectores = []
        for f in all_files:
            if len(re.findall('Clusterizados2_', f)) == 1:
                self.sectores.append(re.split('Clusterizados2_', re.split('\.', f)[0])[-1])
        print(self.sectores)

    def construir(self):

        self.frame_f1 = Label(self.root, text='Indique el sector que quiere analizar', font='arial 20 bold', width=50, pady=50)
        self.frame_f1.grid(row=0, column=0, columnspan=3)


        self.botones = []
        contador_filas = 1
        contador_columnas = 0
        contador_total = 0
        for sector in self.sectores:

            if contador_total == len(self.sectores) - 1 and len(self.sectores) % 3 == 1:
                self.boton = Button(self.root, text=sector, font='arial 12 bold', padx=15, pady=10, borderwidth=5,
                                    width=15)
                self.boton.grid(row=contador_filas, column=1)
                self.boton["command"] = lambda s = sector: self.siguiente(s)

            else:
                self.boton = Button(self.root, text=sector, font='arial 12 bold', padx=15, pady=10, borderwidth=5,
                                    width=15)
                self.boton.grid(row=contador_filas, column=contador_columnas)
                self.boton["command"] = lambda s = sector: self.siguiente(s)

            self.botones.append(self.boton)

            contador_columnas += 1
            if contador_columnas == 3:
                contador_filas += 1
                contador_columnas = 0
            contador_total += 1

        extra = Label(self.root, text='\n\n\n\n')
        extra.grid(row=((len(self.sectores) // 3) + 2), column=0)

    def siguiente(self, sector):
        global contador_ventanas
        self.mapa_sector = Visualizacion(sector)
        ventana_flujos = VentanaFlujos(lista_ventanas[0].root, contador_ventanas, sector)

        lista_ventanas.append(ventana_flujos)
        contador_ventanas += 1
        for b in self.botones:
            if b['text'] == sector:
                b["state"] = "disabled"

        lista_ventanas[0].root.wm_attributes("-topmost", False)
        self.root.wm_attributes("-topmost", False)
        self.root.update()
        lista_ventanas[0].root.update()

    def hide(self):
        self.root.withdraw()

    def show(self):
        self.root.update()
        self.root.deiconify()

    def cerrar(self):
        self.root.destroy()
        contador = 0
        for v in lista_ventanas:
            if v.id == self.id:
                break
            contador += 1
        lista_ventanas.pop(contador)
        lista_ventanas[0].boton1["state"] = "normal"

class VentanaPrincipal():
    def __init__(self):
        self.root = Tk()
        self.id = 0
        self.modo = 'INICIAL'
        self.iniciar_root()

        self.construir_ventana()


    def iniciar_root(self):
        self.root.geometry('600x500')
        self.root.resizable(width=False, height=False)
        self.root.wm_attributes("-topmost", True)
        self.root.title("Ventana inicio")

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)

    def construir_ventana(self):
        self.frame_f1 = LabelFrame(self.root).pack(padx=50, pady=30)
        self.frame_f2 = LabelFrame(master=self.root).pack()
        self.frame_f3 = LabelFrame(master=self.root).pack()

        self.label_inicial = Label(self.frame_f1, text='Pestaña de inicialización.\nElija una de las dos opciones sugeridas a continuación.', font="arial 15")
        self.label_inicial.pack(pady=25)

        self.boton1 = Button(self.frame_f2, width=50, height=5, text='Análisis de un sector individual', font="arial 12", )
        self.boton2 = Button(self.frame_f3, width=50, height=5, text='Análisis conjunto de varios sectores', font="arial 12")
        self.boton1.pack(padx=50, pady=25)
        self.boton2.pack(padx=25)

        self.boton1["command"] = lambda modo = 1: self.iniciar(modo)
        self.boton2["command"] = lambda modo = 2: self.iniciar(modo)

    def iniciar(self, modo=None):

        repetido = False
        for i in lista_ventanas:
            if i.modo == modo:
                repetido = True

        global contador_ventanas
        if not repetido:
            if modo == 1:
                ventana_datos = VentanaIndividual(self.root, contador_ventanas)
                self.boton1["state"] = "disabled"
            else:
                ventana_datos = VentanaConjunto(self.root, contador_ventanas)
                self.boton2["state"] = "disabled"

            lista_ventanas.append(ventana_datos)
            contador_ventanas += 1
            print(contador_ventanas)

        else:
            pass

    def cerrar(self):
        self.root.destroy()


if __name__ == "__main__":
    ventana = VentanaPrincipal()
    lista_ventanas.append(ventana)
    ventana.root.mainloop()