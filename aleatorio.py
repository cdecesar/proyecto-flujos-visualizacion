import functools
import random, pathlib
import time
from datetime import datetime
import tkinter as tk
FILES_PATH = str(pathlib.Path(__file__).parent.resolve())


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


class PopUp():
    def __init__(self, root):

        self.contador = []
        self.contador2 = []
        self.continuar = False

        self.job = None

        self.top = tk.Toplevel(root)
        self.top.geometry('+1200+400')
        self.top.resizable(width=False, height=False)
        # root.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
        self.top.wm_attributes("-topmost", True)
        self.top.title("Popup")
        self.top.protocol("WM_DELETE_WINDOW", self.cerrar)


        self.only_pane = tk.PanedWindow(self.top, orient=tk.VERTICAL)
        self.only_pane.grid(column=0, row=0, rowspan=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.only_pane.rowconfigure(0, weight=1)
        self.only_pane.columnconfigure(0, weight=1)

        self.frame1 = tk.Frame(master=self.top, bg="dimgray", borderwidth=2, relief="raised")
        self.frame1.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.columnconfigure(0, weight=1)
        self.only_pane.add(self.frame1, width=150, height=100)

        self.button = tk.Button(self.frame1, text="PULSAME", fg="aquamarine2", bg="dimgray", font="arial 10 bold")
        self.button.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.button['command'] = self.bucle

        self.top.withdraw()

        # self.bucle()

    def guardar(self, modo):
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
            if segundos < 10:
                segundos = '0' + str(segundos)
            else:
                segundos = str(segundos)

            if minutos < 10:
                minutos = '0' + str(minutos)
            else:
                minutos = str(minutos)

            if hora < 10:
                hora = '0' + str(hora)
            else:
                hora = str(hora)

            if modo == 1:
                mensaje = "PULSADO " + str(len(self.contador) + 1) + " -- " + hora + ":" + minutos + ":" + segundos
                self.contador.append(mensaje)
            else:
                mensaje = "NO PULSADO " + str(len(self.contador2) + 1) + " -- " + hora + ":" + minutos + ":" + segundos
                self.contador2.append(mensaje)

    def bucle(self):
        self.guardar(1)
        if self.job is not None:
            self.top.after_cancel(self.job)
            self.job = None
        self.hide()

    def hide(self):
        if self.job is not None:
            self.guardar(2)
        self.top.withdraw()
        time.sleep(random.randint(1, 5))
        self.show()

    def show(self):
        x = random.randint(100, 1000)
        y = random.randint(100, 600)
        self.top.geometry('+' + str(x) + '+' + str(y))

        self.top.update()
        self.top.deiconify()

        self.job = self.top.after(5000, self.hide)

    def cerrar(self):

        cerrar(self.contador, self.contador2)
        self.top.destroy()

def cerrar(acciones_tomadas, acciones_no_tomadas):
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
                            command=lambda: salir_guardar(nombre, apellido, ejercicio, top, acciones_tomadas, acciones_no_tomadas), fg="aquamarine2",
                            bg="dimgray",
                            font="arial 10")
    boton_cancelar = tk.Button(top, text="Cancelar", command=lambda: minimizar(top), fg="aquamarine2", bg="dimgray",
                               font="arial 10")
    boton_salir.grid(row=3, column=0, padx=5, pady=5)
    boton_cancelar.grid(row=3, column=1, padx=5, pady=5)


def salir_guardar(n, a, e, top, acciones_tomadas, acciones_no_tomadas):
    f = open(
        FILES_PATH + "\\Acciones - Ejercicio " + str(e.get()) + " - " + str(
            n.get()) + " " + str(a.get()) + ".txt", 'w')
    f.write("Ejercicio:" + str(e.get()) + "         Alumno: " + str(n.get()) + " " + str(a.get()) + "\n\n")
    f.write('Total de veces pulsado: ' + str(len(acciones_tomadas) + 1) + '\n')

    for i in range(len(acciones_tomadas)):
        f.write(acciones_tomadas[i] + "\n")
        f.write('\n')
    f.write('Total de veces no pulsado: ' + str(len(acciones_no_tomadas) + 1) + '\n')

    for i in range(len(acciones_no_tomadas)):
        f.write(acciones_no_tomadas[i] + "\n")
    f.close()

    top.destroy()
    root.destroy()


def minimizar(top):
    app1.continuar = True
    top.destroy()

def iniciar():
    tiempos.set_tiempo_inicio()
    app1.show()
    root.withdraw()


tiempos = GuardarTiempo()

root = tk.Tk()
root.geometry('+1200+400')
root.resizable(width=False, height=False)
#root.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
root.wm_attributes("-topmost", True)
root.title("INICIO")

left_pane1 = tk.PanedWindow(root, orient=tk.VERTICAL)
left_pane1.grid(column=0, row=0, rowspan=1, sticky=(tk.N, tk.W, tk.E, tk.S))
left_pane1.rowconfigure(0, weight=1)
left_pane1.columnconfigure(0, weight=1)

frame1 = tk.Frame(master=root, bg="dimgray", borderwidth=2, relief="raised")
frame1.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
frame1.rowconfigure(0, weight=1)
frame1.columnconfigure(0, weight=1)
left_pane1.add(frame1, width=120, height=70)

boton_conflicto = tk.Button(master=frame1, text="COMENZAR", fg="aquamarine2", bg="dimgray")
boton_conflicto.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
boton_conflicto["command"] = iniciar

app1 = PopUp(root)


root.mainloop()