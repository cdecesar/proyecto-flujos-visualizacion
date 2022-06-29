import os, json, glob, pathlib, math, re
from tkinter import *
import pandas
from Visualizacion import Visualizacion
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import numpy as np
from openpyxl.workbook import Workbook



# Quitar los conflictos CLAM, filtrar los otros conflictos por aeronaves que forman parte del sector, y guardar todas las horas

FILES_PATH = str(pathlib.Path(__file__).parent.resolve())

df = pandas.DataFrame()
TIEMPOS = [*range(0, 46)]
LTCA = [0] * 46
CLAM = [0] * 46
AOC = [0] * 46
HDG = [0] * 46
CFL = [0] * 46
COF = [0] * 46

with open(FILES_PATH + '\\Skyvisual_SIMULADOR_02_Event_Log_20220628.log') as f:
    f = f.readlines()

for line in f:
    tiempo = re.findall('\d{2}:\d{2}:\d{2}\.\d{3}', line)
    if len(tiempo) != 0:
        minuto = tiempo[0][3:5]
        preparado = line.split(' \t')[1]
        evento = preparado.split('\t')[0]

        if 'CONFLICT' in evento:
            partido = evento.split('CONFLICT=')[1]

            if partido == 'LTCA':
                LTCA[int(minuto)] += 1

            elif partido == 'CLAM':
                CLAM[int(minuto)] += 1

            else:
                print(partido)


        elif 'EVENT' in line:
            partido = evento.split('EVENT=')[1]

            if partido == 'AOC':
                AOC[int(minuto)] += 1

            elif partido == 'HDG':
                HDG[int(minuto)] += 1

            elif partido == 'CFL':
                CFL[int(minuto)] += 1

            elif partido == 'COF':
                COF[int(minuto)] += 1

            else:
                pass
        else:
            pass



TIEMPOS.append('TOTAL')
LTCA.append(sum(LTCA))
CLAM.append(sum(CLAM))
AOC.append(sum(AOC))
COF.append(sum(COF))
CFL.append(sum(CFL))
HDG.append(sum(HDG))

total = []

for i in range(0, 47):
    total.append(LTCA[i] + CLAM[i] + AOC[i] + CFL[i] + COF[i] + HDG[i])

df['Minuto'] = TIEMPOS
df['Conflicto: LTCA'] = LTCA
df['Conflicto: CLAM'] = CLAM
df['Evento: AOC'] = AOC
df['Evento: HDG'] = HDG
df['Evento: CFL'] = CFL
df['Evento: COF'] = COF
df['Total'] = total

df.to_excel('DatosEjercicio7.xlsx','Sheet1')

