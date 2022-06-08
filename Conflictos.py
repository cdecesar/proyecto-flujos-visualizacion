from datetime import datetime
import tkinter as tk

ITERACION = 0
THREAD = 0

hora_i = 0
minuto_i = 0
segundo_i = 0

lista_conflictos = []
contador_conflictos = 0

lista_entradas = []
contador_entradas = 0

lista_transferencias = []
contador_transferencias = 0


class PopUp():
    def __init__(self, root):
        self.top = tk.Toplevel(root)

        self.top.title("Conflicto")
        self.top.configure(bg='dimgray')
        self.top.wm_attributes("-topmost", True)
        self.top.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
        self.top.resizable(width=False, height=False)
        self.top.geometry('+350+70')

        self.only_pane = tk.PanedWindow(self.top, orient=tk.VERTICAL)
        self.only_pane.grid(column=0, row=0, rowspan=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.only_pane.rowconfigure(0, weight=1)
        self.only_pane.columnconfigure(0, weight=1)

        self.frame1 = tk.Frame(master=self.top, bg="dimgray", borderwidth=2, relief="raised")
        self.frame1.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.columnconfigure(0, weight=1)
        self.only_pane.add(self.frame1, width=150, height=100)

        self.label = tk.Label(self.frame1, text="BOTÓN PULSADO", fg="aquamarine2", bg="dimgray", font="arial 10 bold")
        self.label.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))

        self.destruir()

    def destruir(self):
        self.top.after(1000, self.top.destroy)


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


class VentanaTransferecencia():
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Transferencia")
        self.top.configure(bg='dimgray')
        self.top.wm_attributes("-topmost", True)
        self.top.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
        self.top.resizable(width=False, height=False)
        self.top.geometry('+100+400')

        self.estado = False
        self.cargar()

    def cargar(self):

        if self.estado == False:
            self.top.withdraw()

        self.left_pane1 = tk.PanedWindow(self.top, orient=tk.VERTICAL)
        self.left_pane1.grid(column=0, row=0, rowspan=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.left_pane1.rowconfigure(0, weight=1)
        self.left_pane1.columnconfigure(0, weight=1)

        self.frame1 = tk.Frame(master=self.top, bg="dimgray", borderwidth=2, relief="raised")
        self.frame1.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.columnconfigure(0, weight=1)
        self.left_pane1.add(self.frame1, width=120, height=70)

        self.label_transferencia = tk.Label(master=self.frame1, text="TRANSFERENCIA \n AJUSTADA", fg="aquamarine2",
                                            bg="dimgray")
        self.label_transferencia.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))

        self.bot_pane = tk.PanedWindow(self.top, orient=tk.VERTICAL)
        self.bot_pane.grid(column=0, row=1, rowspan=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.bot_pane.rowconfigure(0, weight=1)
        self.bot_pane.columnconfigure(0, weight=1)

        self.bot_frame = tk.Frame(master=self.top, bg="dimgray", borderwidth=2, relief="raised")
        self.bot_frame.grid(row=1, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.bot_frame.rowconfigure(0, weight=1)
        self.bot_frame.columnconfigure(0, weight=1)
        self.bot_pane.add(self.bot_frame, width=100, height=60)

        self.bboton_1 = tk.Button(master=self.bot_frame, text="SI", width=7, height=4, fg="aquamarine2", bg="dimgray",
                                  command=lambda: self.guardar_transferencias("SI"))
        self.bboton_1.grid(row=0, column=0)
        self.bboton_2 = tk.Button(master=self.bot_frame, text="NO", width=7, height=4, fg="aquamarine2", bg="dimgray",
                                  command=lambda: self.guardar_transferencias("NO"))
        self.bboton_2.grid(row=0, column=1)

    def activar(self):
        self.estado = True
        self.top.update()
        self.top.deiconify()

    def guardar_transferencias(self, s):
        if tiempos.data > 0:
            a = calcular_tiempo()
            contador = len(lista_transferencias)

            mensaje = "Transferencia ajustada: " + str(contador + 1) + " -- " + s + " " + str(a[0]) + ":" + str(
                a[1]) + ":" + str(a[2])
            lista_transferencias.append(mensaje)
            popup = PopUp(root)


class VentanaEntrada():
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Entrada")
        self.top.configure(bg='dimgray')
        self.top.wm_attributes("-topmost", True)
        self.top.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
        self.top.resizable(width=False, height=False)
        self.top.geometry('+400+400')

        self.estado = False
        self.cargar()

    def cargar(self):

        if self.estado == False:
            self.top.withdraw()

        self.left_pane1 = tk.PanedWindow(self.top, orient=tk.VERTICAL)
        self.left_pane1.grid(column=0, row=0, rowspan=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.left_pane1.rowconfigure(0, weight=1)
        self.left_pane1.columnconfigure(0, weight=1)

        self.frame1 = tk.Frame(master=self.top, bg="dimgray", borderwidth=2, relief="raised")
        self.frame1.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.columnconfigure(0, weight=1)
        self.left_pane1.add(self.frame1, width=120, height=70)

        self.label_entrada = tk.Label(master=self.frame1, text="DISCREPANCIA \n PLAN DE VUELO", fg="aquamarine2",
                                      bg="dimgray")
        self.label_entrada.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))

        self.bot_pane = tk.PanedWindow(self.top, orient=tk.VERTICAL)
        self.bot_pane.grid(column=0, row=1, rowspan=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.bot_pane.rowconfigure(0, weight=1)
        self.bot_pane.columnconfigure(0, weight=1)

        self.bot_frame = tk.Frame(master=self.top, bg="dimgray", borderwidth=2, relief="raised")
        self.bot_frame.grid(row=1, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.bot_frame.rowconfigure(0, weight=1)
        self.bot_frame.columnconfigure(0, weight=1)
        self.bot_pane.add(self.bot_frame, width=100, height=60)

        self.bboton_1 = tk.Button(master=self.bot_frame, text="SI", width=7, height=4, fg="aquamarine2", bg="dimgray",
                                  command=lambda: self.guardar_entrada("SI"))
        self.bboton_1.grid(row=0, column=0)
        self.bboton_2 = tk.Button(master=self.bot_frame, text="NO", width=7, height=4, fg="aquamarine2", bg="dimgray",
                                  command=lambda: self.guardar_entrada("NO"))
        self.bboton_2.grid(row=0, column=1)

    def activar(self):
        self.estado = True
        self.top.update()
        self.top.deiconify()

    def guardar_entrada(self, s):
        if tiempos.data > 0:
            a = calcular_tiempo()
            contador = len(lista_entradas)

            mensaje = "Discrepancia plan de vuelo " + str(contador + 1) + " -- " + s + " " + str(a[0]) + ":" + str(
                a[1]) + ":" + str(a[2])
            lista_entradas.append(mensaje)
            popup = PopUp(root)


class VentanaConflicto():
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Conflicto")
        self.top.configure(bg='dimgray')
        self.top.wm_attributes("-topmost", True)
        self.top.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
        self.top.resizable(width=False, height=False)
        self.top.geometry('+800+400')
        self.top.protocol("WM_DELETE_WINDOW", cerrar)

        self.estado = False
        self.cargar()

    def cargar(self):

        if self.estado == False:
            self.top.withdraw()

        self.left_pane1 = tk.PanedWindow(self.top, orient=tk.VERTICAL)
        self.left_pane1.grid(column=0, row=0, rowspan=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.left_pane1.rowconfigure(0, weight=1)
        self.left_pane1.columnconfigure(0, weight=1)

        self.frame1 = tk.Frame(master=self.top, bg="dimgray", borderwidth=2, relief="raised")
        self.frame1.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.frame1.rowconfigure(0, weight=1)
        self.frame1.columnconfigure(0, weight=1)
        self.left_pane1.add(self.frame1, width=120, height=70)

        self.boton_conflicto = tk.Button(master=self.frame1, text="CONFLICTO", fg="aquamarine2", bg="dimgray")
        self.boton_conflicto.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
        self.boton_conflicto["command"] = self.guardar_conflicto

    def activar(self):
        self.estado = True
        self.top.update()
        self.top.deiconify()

    def guardar_conflicto(self):
        if tiempos.data > 0:
            a = calcular_tiempo()
            contador = len(lista_conflictos)

            mensaje = "CONFLICTO " + str(contador + 1) + " -- " + str(a[0]) + ":" + str(a[1]) + ":" + str(a[2])
            lista_conflictos.append(mensaje)
            popup = PopUp(root)


def calcular_tiempo():
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


def cerrar():
    top = tk.Toplevel(root)
    top.title("Guardar")
    top.configure(bg='dimgray')
    top.wm_attributes("-topmost", True)
    top.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
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
    boton_cancelar = tk.Button(top, text="Cancelar", command=lambda: minimizar(top), fg="aquamarine2", bg="dimgray",
                               font="arial 10")
    boton_salir.grid(row=3, column=0, padx=5, pady=5)
    boton_cancelar.grid(row=3, column=1, padx=5, pady=5)


def salir_guardar(n, a, e, top):

    f = open(
        "C:\\Users\\SkySim\\Desktop\\CURSO 21-22\\Acciones - Ejercicio " + str(e.get()) + " - " + str(
            n.get()) + " " + str(a.get()) + ".txt", 'w')
    f.write("Ejercicio:" + str(e.get()) + "         Alumno: " + str(n.get()) + " " + str(a.get()) + "\n")

    for i in range(len(lista_conflictos)):
        f.write(lista_conflictos[i] + "\n")
    f.write("\n")
    for i in range(len(lista_entradas)):
        f.write(lista_entradas[i] + "\n")
    f.write("\n")
    for i in range(len(lista_transferencias)):
        f.write(lista_transferencias[i] + "\n")
    f.close()

    top.destroy()
    root.destroy()


def minimizar(top):
    top.destroy()


def iniciar():
    tiempos.set_tiempo_inicio()
    app1.activar()
    app2.activar()
    app3.activar()
    root.withdraw()


tiempos = GuardarTiempo()

root = tk.Tk()
root.geometry('+1200+400')
root.resizable(width=False, height=False)
root.iconbitmap('C:\\Users\\SkySim\\Desktop\\Ventanas\\Logo_SATAA.ico')
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

boton_conflicto = tk.Button(master=frame1, text="START", fg="aquamarine2", bg="dimgray")
boton_conflicto.grid(row=0, column=0, sticky=(tk.W, tk.S, tk.E, tk.N))
boton_conflicto["command"] = iniciar

app1 = VentanaConflicto(root)
app2 = VentanaEntrada(root)
app3 = VentanaTransferecencia(root)

root.mainloop()
