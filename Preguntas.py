datos_ej1 = [[5, "Primera pregunta"], [15, "Segunda pregunta"]]
datos_ej2 = [1]
import time
from datetime import datetime
import logging
import tkinter as tk
from tkinter import ttk
import threading
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

lista_respuestas = []
contador_respuestas = 0
lista_sin_responder = []

hora_i = 0
minuto_i = 0
segundo_i = 0


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


class Ventana():
    def __init__(self, root):
        self.top = tk.Toplevel(root)

        self.parent = root
        self.top.title("Workload")
        self.top.configure(bg='dimgray')
        self.top.wm_attributes("-topmost", True)
        #self.top.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
        self.top.resizable(width=False, height=False)
        self.top.geometry('+0+500')

        self.comienzo_ejecucion_s = 0
        self.comienzo_ejecucion_m = 0

        self.top.withdraw()

        self.iteracion = 0

        self.estado = True
        self.mensaje = data[self.iteracion][1]
        self.cargar()

    def cargar(self):

        self.top_pane = tk.PanedWindow(self.top, orient=tk.VERTICAL)
        self.top_pane.grid(column=0, row=0, rowspan=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.top_pane.rowconfigure(0, weight=1)
        self.top_pane.columnconfigure(0, weight=1)

        self.top_frame = tk.Frame(master=self.top, bg="dimgray", borderwidth=2, relief="raised")
        self.top_frame.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.columnconfigure(0, weight=1)
        self.top_pane.add(self.top_frame, width=220, height=90)

        self.lab = tk.Label(master=self.top_frame, text=self.mensaje, fg="aquamarine2", bg="dimgray", width=10,
                            height=10)
        self.lab.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.bot_pane = tk.PanedWindow(self.top, orient=tk.VERTICAL)
        self.bot_pane.grid(column=0, row=1, rowspan=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.bot_pane.rowconfigure(0, weight=1)
        self.bot_pane.columnconfigure(0, weight=1)

        self.bot_frame = tk.Frame(master=self.top, bg="dimgray", borderwidth=2, relief="raised")
        self.bot_frame.grid(row=1, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.bot_frame.rowconfigure(0, weight=1)
        self.bot_frame.columnconfigure(0, weight=1)
        self.bot_pane.add(self.bot_frame, width=100, height=60)

        self.bboton_1 = tk.Button(master=self.bot_frame, width=9, height=8, fg="aquamarine2", bg="green",
                                  command=lambda: self.guardar_respuesta('VERDE'))
        self.bboton_1.grid(row=0, column=0)
        self.bboton_2 = tk.Button(master=self.bot_frame, width=9, height=8, fg="aquamarine2", bg="yellow",
                                  command=lambda: self.guardar_respuesta('AMARILLO'))
        self.bboton_2.grid(row=0, column=1)
        self.bboton_3 = tk.Button(master=self.bot_frame, width=9, height=8, fg="aquamarine2", bg="red",
                                  command=lambda: self.guardar_respuesta('ROJO'))
        self.bboton_3.grid(row=0, column=2)

    def mostrar(self):
        respuestas = len(lista_respuestas)
        self.estado = True
        self.top.update()
        self.top.deiconify()

        self.top.after(20000, self.sin_respuesta, respuestas)

    def sin_respuesta(self, respuestas1):

        respuestas2 = len(lista_respuestas)
        if respuestas1 == respuestas2:
            m = self.mensaje + ": " + "No se ha pulsado boton"
            lista_sin_responder.append(m)
            self.esconder()

    def guardar_respuesta(self, boton):
        if self.estado:
            a = self.calcular_tiempo()

            m = self.mensaje + " Boton " + str(boton) + " -- " + str(a[0]) + ":" + str(a[1]) + ":" + str(a[2])
            lista_respuestas.append(m)
            self.esconder()

    def esconder(self):
        self.iteracion += 1
        if self.iteracion < len(data):
            self.lab["text"] = data[self.iteracion][1]
            self.mensaje = data[self.iteracion][1]
            self.top.withdraw()
            self.estado = False
            self.esconder2()
        else:
            self.top.destroy()
            cerrar()

    def esconder2(self):
        dormir = self.tiempo_dormir(data[self.iteracion][0])
        time.sleep(dormir)
        self.mostrar()

    def tiempo_dormir(self, t):
        if tiempos.data > 0:
            h = datetime.now().hour * 60 * 60
            m = datetime.now().minute * 60
            s = datetime.now().second

            actual = h + m + s

            actual = actual - tiempos.data

            result = t - actual

            return result

    def calcular_tiempo(self):
        if tiempos.data > 0:
            h = datetime.now().hour * 60 * 60
            m = datetime.now().minute * 60
            s = datetime.now().second

            actual = h + m + s

            actual = actual - tiempos.data

            segundos = actual % 60
            minutosf = actual // 60
            hora = minutosf // 60
            minutos = minutosf % 60

            return hora, minutos, segundos


def tiempo_final():
    if tiempos.data > 0:
        h = datetime.now().hour * 60 * 60
        m = datetime.now().minute * 60
        s = datetime.now().second

        actual = h + m + s

        actual = actual - tiempos.data

        result = 2760 - actual

        return result

def cerrar():
    t_final = tiempo_final()
    time.sleep(t_final)
    top = tk.Toplevel(root)
    top.title("Guardar")
    top.configure(bg='dimgray')
    top.wm_attributes("-topmost", True)
    #top.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
    top.resizable(width=False, height=False)

    ejercicio = tk.Entry(top)
    ejercicio.place(x=100, y=50)
    ejercicio.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(top, text="Ejercicio", fg="aquamarine2", bg="dimgray", font="arial 10 bold").grid(row=0, column=0)
    tk.Label(top, text="Nombre", fg="aquamarine2", bg="dimgray", font="arial 10 bold").grid(row=1, column=0)
    tk.Label(top, text="Apellidos", fg="aquamarine2", bg="dimgray", font="arial 10 bold").grid(row=1, column=1)

    nombre = tk.Entry(top)
    nombre.place(x=50, y=50)
    nombre.grid(row=2, column=0, padx=5, pady=5)

    apellido = tk.Entry(top)
    apellido.place(x=100, y=50)
    apellido.grid(row=2, column=1, padx=5, pady=5)

    boton_salir = tk.Button(top, text="Guardar y salir",
                            command=lambda: salir_guardar(nombre, apellido, ejercicio, top), fg="aquamarine2",
                            bg="dimgray",
                            font="arial 10")

    boton_salir.grid(row=3, column=0, padx=5, pady=5)


def salir_guardar(n, a, e, top):
    f = open(
        "C:\\Users\\SkySim\\Desktop\\CURSO 21-22\\Respuestas Workload - Ejercicio " + e.get() + " - " + n.get() + " " + a.get() + ".txt",
        'w')
    f.write("Ejercicio:" + e.get() + "         Alumno: " + n.get() + " " + a.get() + "\n")

    for i in range(len(lista_respuestas)):
        f.write(lista_respuestas[i] + "\n")
    f.write("\n")
    for i in range(len(lista_sin_responder)):
        f.write(lista_sin_responder[i] + "\n")
    f.close()

    top.destroy()
    root.destroy()


def inicio():
    tiempos.set_tiempo_inicio()
    root.withdraw()
    time.sleep(data[0][0])
    app.mostrar()


tiempos = GuardarTiempo()
ejercicio = input("Ejercicio a ejecutar: ")
datos_ej1 = [[2, "Evalúe la carga de trabajo"], [300, "Evalúe la carga de trabajo"], [450, "Evalúe la carga de trabajo"], [600, "Evalúe la carga de trabajo"], [750, "Evalúe la carga de trabajo"], [900, "Evalúe la carga de trabajo"], [1050, "Evalúe la carga de trabajo"], [1200, "Evalúe la carga de trabajo"], [1350, "Evalúe la carga de trabajo"], [1500, "Evalúe la carga de trabajo"], [1650, "Evalúe la carga de trabajo"], [1800, "Evalúe la carga de trabajo"], [1950, "Evalúe la carga de trabajo"], [2100, "Evalúe la carga de trabajo"], [2250, "Evalúe la carga de trabajo"], [2400, "Evalúe la carga de trabajo"],[2550, "Evalúe la carga de trabajo"]]
datos_ej3 = [1]
datos_ej4 = [1]
datos_ej5 = [1]
datos_ej6 = [1]
datos_ej7 = [1]
datos_ej8 = [1]
datos_ej9 = [1]
datos_ej10 = [1]

if ejercicio == "EJERCICIO":
    data = datos_ej1
elif ejercicio == "Ejercicio 2":
    data = datos_ej2
elif ejercicio == "Ejercicio 3":
    data = datos_ej3
elif ejercicio == "Ejercicio 4":
    data = datos_ej4
elif ejercicio == "Ejercicio 5":
    data = datos_ej5
elif ejercicio == "Ejercicio 6":
    data = datos_ej6
elif ejercicio == "Ejercicio 7":
    data = datos_ej7
elif ejercicio == "Ejercicio 8":
    data = datos_ej8
elif ejercicio == "Ejercicio 9":
    data = datos_ej9
else:
    ejercicio == "Ejercicio 10"
    data = datos_ej10

root = tk.Tk()
root.geometry('+1200+400')
root.resizable(width=False, height=False)
#root.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
root.wm_attributes("-topmost", True)
root.title("Workload")

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
boton_conflicto["command"] = inicio

app = Ventana(root)

root.mainloop()
