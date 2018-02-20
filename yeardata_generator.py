# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 15:41:07 2018

@author: User
"""

import math
import random
import pandas as pd
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
# from datetime import date


def gen_yeardata(personas=0, graphs=True):
    if personas == 0:
        personas = int(input('Ingrese el numero de personas en el hogar:  '))

    # imports hourly data
    cols = ['DOY', 'MES', 'día', 'Hora', 'IDT', 'GHI', 'DNI', 'GTI20', 'GTI35', 'GTI45', 'GTI60', 'GTI90', 'TAM', 'HRE', 'PAM', 'VVI10', 'DVI10', 'VVI20', 'DVI20', 'CZ', 'AS', 'GS']
    data = pd.read_csv(r'data\AMTUes_v2-4_MVD_horario.csv')
    data.columns = cols

    dclim = data.loc[:, ['DOY', 'MES', 'Hora', 'GTI45', 'TAM', 'VVI10']]

    # promedio de temp amb mensual
    Temps = data.groupby(by=['MES'])['TAM'].agg(np.mean).reset_index()
    # se entra con Temps.iloc[mes-1,1]

    #  (°F - 32) x 5/9 = °C
    #  (°C × 9/5) + 32 = °F
    # Temp promedio anual
    Tav = (Temps['TAM'].mean()) * 9 / 5 + 32
    ratio = 0.4 + 0.01 * (Tav - 44)

    # Delta Tmax
    DTmax = ((Temps['TAM'].max()) * 9 / 5 + 32 - (Temps['TAM'].min()) * 9 / 5 + 32) / 2

    lag = 35 - (Tav - 44)
    # Temp de agua de entrada
    dclim['Tmains'] = ((Tav + 6 + ratio * DTmax / 2 * np.sin((0.986 * (dclim['DOY'] - 15 - lag) + 90) * math.pi / 180) - 32) * 5 / 9)

    consumos = perfil_anual(personas)

    yeardata = pd.merge(dclim, consumos[1], on=['DOY', 'Hora'], how='left')
    yeardata.fillna(0, inplace=True)

    # Temps en Celsius xq se restan
    perdidas = 2    # perdidas en tuberia desde calentador a uso
    Tuso = 38
    Tsal = 60       # Temp de seteo del calentador
    Tcal = Tsal - perdidas

    yeardata['Total lts caliente'] = (yeardata['Volumen [lts] caliente']) + (yeardata['Volumen [lts] tibia'] * (Tuso - yeardata['Tmains']) / (Tcal - yeardata['Tmains']))

    # Agrega informacion del colector solar
    yeardata = collector(yeardata)

    hoy = dt.date.today().strftime("%d-%m-%y")
    yeardata.to_csv(r'generated_csvs\Base ' + hoy + ' ' + str(personas) + 'pers.csv')

    anual = yeardata.groupby(['DOY'])['Total lts caliente'].sum().reset_index()

    if graphs:
        style.use('fivethirtyeight')

        plt.figure()
        ax = plt.subplot(1, 1, 1)
        plt.bar(anual['DOY'], anual['Total lts caliente'], linewidth=10)
        plt.xlabel('día del año', fontsize=24)
        plt.yticks(fontsize=20)
        x = [i for i in range(15, 366, 15)]
        x.insert(0, 1)
        plt.xticks(x, fontsize=20)
        plt.ylabel('Consumo de agua caliente lts/día', fontsize=24)
        plt.grid(False, axis='x')
        ax.set_xlim(xmin=0)

        plt.figure()
        ax = plt.subplot(1, 1, 1)
        d = random.randint(1, 365)
        day = yeardata[yeardata['DOY'] == d]
        x2 = day['Hora'].values.tolist()
        plt.bar(day['Hora'].values.tolist(), day['Total lts caliente'].values.tolist())
        fec = dt.date(2018, 1, 1) + dt.timedelta(d - 1)
        tit = 'Perfil del día N ' + str(d) + ' (' + fec.strftime("%d-%b") + ')'
        plt.title(tit, fontsize=28)
        plt.yticks(fontsize=20)
        plt.xticks(x2, fontsize=20)
        plt.xlabel('Hora', fontsize=24)
        plt.ylabel('Consumo de agua caliente lts/hora', fontsize=24)
        plt.grid(False, axis='x')
        label = "Total de litros\nconsumidos en el día:\n" + str(round(day['Total lts caliente'].sum(), 0))
        ax.text(2, day['Total lts caliente'].max() * 0.9, label, ha='center', va='bottom', fontsize=18, weight='bold')
        ax.set_xlim(xmin=0)

        plt.figure()
        yeardata['COP'] = 6.81 - 0.121 * (60 - yeardata['TAM']) + 0.00063 * (60 - yeardata['TAM']) * (60 - yeardata['TAM'])
        yeardata['COP'].plot()
        plt.ylabel('COP', fontsize=24)
        plt.xlabel('Hora del año', fontsize=24)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylim(0, 4.5)
    
        plt.figure()
        ef_col = yeardata.groupby('DOY')['Qu','GTI45'].sum()
        # Apeture area del colector 2.33 m2
        ef_col['Ef'] = round(ef_col['Qu'] / (ef_col['GTI45'] * 2.33) * 100)
        ef_col['Ef'].plot()
        plt.ylabel('Eficiencia diaria (%)', fontsize=24)
        plt.xlabel('DOY', fontsize=24)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylim(0, 70)
    

    return yeardata