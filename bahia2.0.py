import time
from datetime import datetime
import logging
import tkinter as tk
from tkinter import ttk
import threading
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import pandas


class GuardarTiempo():
    def __init__(self):
        self.data = 0

    def set_tiempo_inicio(self):
        if self.data == 0:
            h = datetime.now().hour
            m = datetime.now().minute
            s = datetime.now().second
            h = h * 60 * 60
            m = m * 60
            self.data = s + h + m


class VentanaCompleta():
    def __init__(self, root, boton):
        self.top = tk.Toplevel(root)
        self.top.title("KK")
        self.top.configure(bg='dimgray')
        self.top.wm_attributes("-topmost", True)
        self.top.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
        self.top.resizable(width=False, height=False)
        self.top.geometry('+400+400')
        self.top.protocol("WM_DELETE_WINDOW", self.cerrar)

        self.ventana_anterior = None

        self.boton = int(boton)
        self.cargar_info()

    def cargar_info(self):

        self.frame1 = tk.Frame(master=self.top, bg="dimgray", borderwidth=2, relief="raised")
        self.frame1.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.columnconfigure(0, weight=1)

        contador2 = 0

        for t in data.columns:
            a = data[t]
            b = a[self.boton]
            if contador2 > 2 and contador2 < 9:
                if str(b) != "nan":
                    texto = self.sacarpuntos(str(b))

                    self.label = tk.Label(self.top, text=t, fg="aquamarine2", bg="dimgray", font="arial 10 bold")
                    self.label.grid(row=0, column=contador2, sticky=(tk.W, tk.S, tk.E, tk.N))

                    self.label = tk.Label(self.top, text=texto, fg="white", bg="dimgray",
                                          font="arial 10 bold")
                    self.label.grid(row=1, column=contador2, sticky=(tk.W, tk.S, tk.E, tk.N))

                    contador2 += 1
            else:
                self.label = tk.Label(self.top, text=t, fg="aquamarine2", bg="dimgray",
                                      font="arial 10 bold")
                self.label.grid(row=0, column=contador2, sticky=(tk.W, tk.S, tk.E, tk.N))

                self.label = tk.Label(self.top, text=str(b), fg="white", bg="dimgray",
                                      font="arial 10 bold")
                self.label.grid(row=1, column=contador2, sticky=(tk.W, tk.S, tk.E, tk.N))

                contador2 += 1

    def sacarpuntos(self, texto):
        final = ""

        for letra in texto:
            if letra != "-":
                final = final + letra
            else:
                nueva_linea = "\n"
                final = final + nueva_linea

        return final


    def cerrar(self):
        self.top.destroy()

        self.ventana_anterior.setEstado()
        self.ventana_anterior.activar()


class VentanaSecundaria():
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("KK")
        self.top.configure(bg='dimgray')
        self.top.wm_attributes("-topmost", True)
        self.top.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
        self.top.resizable(width=False, height=False)
        self.top.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.top.geometry('+400+400')

        self.top.withdraw()

        self.contador = 0
        self.lista_botones_t = []
        self.lista_botones = []
        self.lista_estados = []
        self.dicct = {}

        self.estado = False
        self.actualizacion = 0
        self.botones_borrados = 0

        self.cargar()

        #t_primera_actualizacion = self.calcular_tiempo(0)
        #print("TIEMPO" + str(t_primera_actualizacion))
        #self.top.after(t_primera_actualizacion, self.cargar)
        t_primera_eliminacion = self.calcular_tiempo(1)
        print("Teimpo " + str(t_primera_eliminacion))
        self.top.after(t_primera_eliminacion, self.borrar)

    def setEstado(self):
        self.estado = True

    def activar(self):
        if self.estado == True:
            self.top.update()
            self.top.deiconify()

    def cargar(self):

        self.frame1 = tk.Frame(master=self.top, bg="dimgray", borderwidth=2, relief="raised")
        self.frame1.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.columnconfigure(0, weight=1)

        for i in lista:
        #i = lista[self.contador]

            self.boton_actualizar_estado = tk.Button(master=self.frame1, fg="aquamarine2", bg="dimgray", width=4, font="arial 11 bold")
            self.boton_actualizar_estado.grid(row=self.contador, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
            self.boton_actualizar_estado['text'] = "T"
            self.boton_actualizar_estado['command'] = lambda t = self.contador: self.actualizar_estado(t)
            self.lista_estados.append(0)
            self.lista_botones_t.append(self.boton_actualizar_estado)


            self.boton_conflicto = tk.Button(master=self.frame1, fg="aquamarine2", bg="dimgray", width=10, height=1, font="arial 11 bold")
            self.boton_conflicto.grid(row=self.contador, column=1, sticky=(tk.W, tk.S, tk.E, tk.N))

            self.lista_botones.append(self.boton_conflicto)
            self.boton_conflicto["text"] = i
            self.boton_conflicto["command"] = lambda q = str(self.contador): self.nueva_ventana(q)

            clave = str(salidas_transformadas1[self.contador])
            self.dicct.update({clave: self.contador})

            self.contador += 1
        #print("Contador al añadir callsign" + str(self.contador))
        #tiempo_hasta_actualizacion = self.calcular_tiempo(0)
        #print("Tiempo hasta: " + str(tiempo_hasta_actualizacion))
        #self.top.after(tiempo_hasta_actualizacion, self.cargar)

    def borrar(self):
        valor = self.dicct.get(str(salidas_transformadas2[self.botones_borrados]))
        self.botones_borrados += 1

        b = self.lista_botones[valor]
        b.grid_remove()
        t = self.lista_botones_t[valor]
        t.grid_remove()

        tiempo_hasta_actualizacion = self.calcular_tiempo(1)
        self.top.after(tiempo_hasta_actualizacion, self.borrar)

    def calcular_tiempo(self, accion):
        h = datetime.now().hour
        m = datetime.now().minute
        s = datetime.now().second
        h = h * 60 * 60
        m = m * 60
        t_actual = s + h + m - tiempos.data
        if accion == 0:
            momento_deseado = entradas_transformadas[self.contador]
            print("MOMENTO0" + str(momento_deseado))
        else:
            momento_deseado = salidas_transformadas2[self.botones_borrados]
            print("MOMENTO1" + str(momento_deseado))
        t_final = momento_deseado - t_actual

        return t_final * 1000


    def actualizar_estado(self, fila):
        est = self.lista_estados[fila]
        b = self.lista_botones[fila]
        if est == 0:
            b.configure(fg='white')
        elif est == 1:
            b.configure(fg='red')
        elif est == 2:
            b.configure(fg='dimgray')
        else:
            return None

        c = 0
        while c < len(self.lista_estados):
            e = self.lista_estados.pop(0)
            if c == fila:
                e += 1
                self.lista_estados.append(e)
            else:
                self.lista_estados.append(e)
            c += 1

    def nueva_ventana(self, boton):
        self.estado = False
        self.top.withdraw()
        app3 = VentanaCompleta(root, boton)
        app3.ventana_anterior = app.otra_v

    def cerrar(self):
        self.estado = False
        self.top.withdraw()

        app.show()


class VentanaPrincipal(object):
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.resizable(width=False, height=False)
        self.root.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
        self.root.wm_attributes("-topmost", True)
        self.root.title("PRUEBA")
        self.root.withdraw()
        self.crear_v()
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.padre = root

        self.otra_v = 0

        self.estado = True

    def crear_v(self):
        self.only_pane = tk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.only_pane.grid(column=0, row=0, rowspan=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.only_pane.rowconfigure(0, weight=1)
        self.only_pane.columnconfigure(0, weight=1)

        self.frame1 = tk.Frame(master=self.root, bg="dimgray", borderwidth=2, relief="raised")
        self.frame1.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.columnconfigure(0, weight=1)
        self.only_pane.add(self.frame1, width=150, height=100)

        self.boton_conflicto = tk.Button(master=self.frame1, fg="aquamarine2", bg="dimgray", width=15, command=self.abrir_bahia)
        self.boton_conflicto.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.boton_conflicto["text"] = "BAHIA DE VUELO"

    def hide(self):
        self.root.withdraw()

    def show(self):
        self.root.update
        self.root.deiconify()

    def abrir_bahia(self):
        self.hide()

        self.otra_v.setEstado()
        self.otra_v.activar()

    def cerrar(self):

        self.otra_v.top.destroy()
        self.root.destroy()
        self.padre.destroy()

def tiempos_entrada(columna):
    tiempos_entrada = data[columna]
    tiempos_transformados = []
    for i in tiempos_entrada:
        m = ""
        s = ""
        t = 0
        cont_ = 0
        t = (i.minute * 60) + i.second + (i.hour * 3600)
        t = t
        tiempos_transformados.append(t)

    return tiempos_transformados


def iniciar():
    tiempos.set_tiempo_inicio()
    app2 = VentanaSecundaria(root)
    app.otra_v = app2
    app.show()
    root.withdraw()


tiempos = GuardarTiempo()

a = str(input("Introduce la hoja de excell que quieras abrir: "))
data = pandas.read_excel("C:\\Users\\SkySim\\Desktop\\Ventanas\\Programas_C\\Ficheros\\Libro1.xlsx", sheet_name=a)
lista = []
contador = 0
n = data['CALLSIGN']
entradas_transformadas = tiempos_entrada('ENTRADA')
salidas_transformadas1 = tiempos_entrada('SALIDA')
salidas_transformadas2 = tiempos_entrada('SALIDA')
print(salidas_transformadas2[0])

salidas_transformadas2.sort()
print(salidas_transformadas1[0])
print(salidas_transformadas2[0])

while (contador < data.shape[0]):
    lista.append(n[contador])
    contador += 1

root = tk.Tk()
root.geometry('+1200+400')
root.resizable(width=False, height=False)
root.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
root.wm_attributes("-topmost", True)
root.title("PRUEBA")

left_pane1 = tk.PanedWindow(root, orient=tk.VERTICAL)
left_pane1.grid(column=0, row=0, rowspan=1, sticky=(tk.N, tk.W, tk.E, tk.S))
left_pane1.rowconfigure(0, weight=1)
left_pane1.columnconfigure(0, weight=1)

frame1 = tk.Frame(master=root, bg="dimgray", borderwidth=2, relief="raised")
frame1.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
frame1.rowconfigure(0, weight=1)
frame1.columnconfigure(0, weight=1)
left_pane1.add(frame1, width=120, height=70)

boton_conflicto = tk.Button(master=frame1, text="START", fg="aquamarine2", bg="dimgray")
boton_conflicto.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
boton_conflicto["command"] = iniciar

app = VentanaPrincipal(root)
#app2 = VentanaSecundaria(root)

root.mainloop()
