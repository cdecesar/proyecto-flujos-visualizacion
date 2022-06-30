import os, json, glob, pathlib, math, re
from tkinter import *
import pandas
from Visualizacion import Visualizacion
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import numpy as np
from openpyxl.workbook import Workbook

def calcularTiempo(tiempo):
    minutos = int(tiempo[0][3:5])
    segundos = int(tiempo[0][6])

    return  minutos * 6 + segundos

# Quitar los conflictos CLAM, filtrar los otros conflictos por aeronaves que forman parte del sector, y guardar todas las horas

FILES_PATH = str(pathlib.Path(__file__).parent.resolve())

repeticiones = {
    'LTCA': {

    },
    'HDG': [],
    'AOC': [],
    'CFO': [],
    'CFL': [],
}

df = pandas.DataFrame()
TIEMPOS = []

for i in range(0, 46):
    for j in range(0, 6):
        TIEMPOS.append(i * 6 + j)

LTCA = [0] * 276
CLAM = [0] * 276
AOC = [0] * 276
HDG = [0] * 276
CFL = [0] * 276
COF = [0] * 276

with open(FILES_PATH + '\\Skyvisual_SIMULADOR_02_Event_Log_20220628.log') as f:
    f = f.readlines()

for line in f:
    tiempo = re.findall('\d{2}:\d{2}:\d{2}\.\d{3}', line)
    if len(tiempo) != 0:
        minuto = calcularTiempo(tiempo)
        preparado = line.split(' \t')[1]
        evento = preparado.split('\t')[0]

        if 'CONFLICT' in evento:
            partido = evento.split('CONFLICT=')[1]
            if partido == 'LTCA':
                LTCA[int(minuto)] += 1
                nave1 = preparado.split('\t')[2].split('CS1=')[1]
                nave2 = preparado.split('\t')[6].split('CS2=')[1]
                if 'START' in line:
                    if nave1 + '-' + nave2 not in repeticiones['LTCA'].keys():
                        repeticiones['LTCA'].update({nave1 + '-' + nave2: [[['START', minuto]]]})
                    else:
                        repeticiones['LTCA'][nave1 + '-' + nave2].append([['START', minuto]])
                else:
                    info = repeticiones['LTCA'][nave1 + '-' + nave2]
                    info[len(info) - 1].append(['END', minuto])
                    repeticiones['LTCA'][nave1 + '-' + nave2] = info

            elif partido == 'CLAM':
                CLAM[int(minuto)] += 1

            else:
                pass

        elif 'EVENT' in line:
            partido = evento.split('EVENT=')[1]
            nave = preparado.split('\t')[1].split('CS=')[1]
            if partido == 'AOC':
                if nave not in repeticiones['AOC']:
                    repeticiones['AOC'].append(nave)
                    AOC[int(minuto)] += 1

            elif partido == 'HDG':
                HDG[int(minuto)] += 1

            elif partido == 'CFL':
                CFL[int(minuto)] += 1

            elif partido == 'COF':
                COF[int(minuto)] += 1

            else:
                pass
            if partido != 'AOC' and partido != 'COF':
                for i in repeticiones['LTCA'].keys():
                    if nave in i:
                        datos = repeticiones['LTCA'][i]
                        ultimoItem = datos[-1][-1]
                        if 'END' not in ultimoItem:
                            repeticiones['LTCA'][i][len(repeticiones['LTCA'][i]) - 1].append(partido + '-' + str(minuto))
                        else:
                            repeticiones['LTCA'][i][len(repeticiones['LTCA'][i]) - 1].insert(-1, partido + '-' + str(minuto))
        else:
            pass

print(len(repeticiones['AOC']))
for i in repeticiones['LTCA'].keys():
    print(i)
    print(repeticiones['LTCA'].get(i))

TIEMPOS.append('TOTAL')
LTCA.append(sum(LTCA))
CLAM.append(sum(CLAM))
AOC.append(sum(AOC))
COF.append(sum(COF))
CFL.append(sum(CFL))
HDG.append(sum(HDG))

total = []

for i in range(0, 277):
    total.append(LTCA[i] + CLAM[i] + AOC[i] + CFL[i] + COF[i] + HDG[i])

df['Minuto'] = TIEMPOS
df['Conflicto: LTCA'] = LTCA
df['Conflicto: CLAM'] = CLAM
df['Evento: AOC'] = AOC
df['Evento: HDG'] = HDG
df['Evento: CFL'] = CFL
df['Evento: COF'] = COF
df['Total'] = total

df.to_excel('DatosEjercicio7.xlsx','Sheet2')

