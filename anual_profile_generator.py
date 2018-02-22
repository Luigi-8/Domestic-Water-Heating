# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 15:35:06 2018

@author: User
"""

import math
import random
import pandas as pd
import datetime as dt
import numpy as np

# Liters per day per person for showers: 5.68 * 8.14
# Liters per day per person for sinks: 28% * 5.68 * 8.14
# Liters per day per person for DW: 18% * 5.68 * 8.14


def perfil_anual(personas):   

    # cantidad de agua total (fria +caliente)
    allevents = []
    agrupado = []
    for day in range(365):
        cons_dia = consumo_dia(personas)
        cons_dia['DOY'] = day + 1
        allevents.append(cons_dia)
        agrupado.append(cons_dia.groupby(['DOY', 'Hora'])
                        ['Volumen [lts] tibia', 'Volumen [lts] caliente'].
                        agg(sum).reset_index(level=['DOY', 'Hora']))

    eventos = pd.concat(allevents)
    consumo_horario = pd.concat(agrupado)

    hoy = dt.date.today().strftime("%d-%m-%y")
    eventos.to_csv(r'generated_csvs\Eventos ' + hoy + ' ' +
                   str(personas) + 'pers.csv')
    consumo_horario.to_csv(r'generated_csvs\Horario ' + hoy + ' ' +
                           str(personas) + 'pers.csv')

    return [eventos, consumo_horario]


def consumo_dia(personas):
    dfsink = sink(personas)
    dfshower = shower(personas)
    dfDW = DW(personas)

    dftotal = pd.concat([dfsink, dfshower, dfDW])
    dftotal.sort_values('Hora', inplace=True)

    return dftotal


def sink_time():
    time = pd.DataFrame([
            [0, 0.0271954674220963, 0.0271954674220963],
            [1, 0.0141643059490085, 0.0413597733711048],
            [2, 0.00679886685552408, 0.0481586402266289],
            [3, 0.00509915014164306, 0.0532577903682719],
            [4, 0.00509915014164306, 0.058356940509915],
            [5, 0.00679886685552408, 0.0651558073654391],
            [6, 0.0181303116147309, 0.08328611898017],
            [7, 0.0424929178470255, 0.125779036827195],
            [8, 0.0623229461756374, 0.188101983002833],
            [9, 0.0657223796033994, 0.253824362606232],
            [10, 0.0617563739376771, 0.315580736543909],
            [11, 0.0543909348441926, 0.369971671388102],
            [12, 0.0498583569405099, 0.419830028328612],
            [13, 0.0487252124645892, 0.468555240793201],
            [14, 0.0453257790368272, 0.513881019830028],
            [15, 0.0413597733711048, 0.555240793201133],
            [16, 0.0430594900849858, 0.598300283286119],
            [17, 0.0481586402266289, 0.646458923512748],
            [18, 0.0651558073654391, 0.711614730878187],
            [19, 0.0747875354107649, 0.786402266288952],
            [20, 0.0691218130311615, 0.855524079320113],
            [21, 0.056657223796034, 0.912181303116147],
            [22, 0.0481586402266289, 0.960339943342776],
            [23, 0.0396600566572238, 1]],
            columns=['Hour', 'Hourly Profile', 'Accumulated'])

    a = random.random()
    time['Dif'] = abs(time['Accumulated'] - a)

    return time['Dif'].idxmin(axis=1)


def shower_time():
    time = pd.DataFrame([
            [0, 0.0208940719144801, 0.0208940719144801],
            [1, 0.010689990281827, 0.0315840621963071],
            [2, 0.00485908649173955, 0.0364431486880467],
            [3, 0.00340136054421769, 0.0398445092322643],
            [4, 0.00485908649173955, 0.0447035957240039],
            [5, 0.0136054421768708, 0.0583090379008746],
            [6, 0.0515063168124393, 0.109815354713314],
            [7, 0.117589893100097, 0.227405247813411],
            [8, 0.116618075801749, 0.34402332361516],
            [9, 0.0947521865889213, 0.438775510204082],
            [10, 0.0743440233236152, 0.513119533527697],
            [11, 0.0597667638483965, 0.572886297376093],
            [12, 0.0471331389698737, 0.620019436345967],
            [13, 0.0340136054421769, 0.654033041788144],
            [14, 0.0291545189504373, 0.683187560738581],
            [15, 0.0252672497570457, 0.708454810495627],
            [16, 0.0262390670553936, 0.73469387755102],
            [17, 0.0301263362487852, 0.764820213799806],
            [18, 0.0388726919339164, 0.803692905733722],
            [19, 0.0422740524781341, 0.845966958211856],
            [20, 0.0422740524781341, 0.88824101068999],
            [21, 0.0417881438289602, 0.93002915451895],
            [22, 0.0408163265306122, 0.970845481049563],
            [23, 0.0291545189504373, 1]],
            columns=['Hour', 'Hourly Profile', 'Accumulated'])

    a = random.random()
    time['Dif'] = abs(time['Accumulated'] - a)

    return time['Dif'].idxmin(axis=1)


def DW_time():
    time = pd.DataFrame([
            [0, 0.030716724, 0.030716724],
            [1, 0.015358362, 0.046075086],
            [2, 0.006825939, 0.052901025],
            [3, 0.005119454, 0.058020479],
            [4, 0.003412969, 0.061433448],
            [5, 0.003412969, 0.064846417],
            [6, 0.010238908, 0.075085325],
            [7, 0.020477816, 0.095563141],
            [8, 0.030716724, 0.126279865],
            [9, 0.058020478, 0.184300343],
            [10, 0.064846416, 0.249146759],
            [11, 0.056313993, 0.305460752],
            [12, 0.04778157, 0.353242322],
            [13, 0.040955631, 0.394197953],
            [14, 0.046075085, 0.440273038],
            [15, 0.037542662, 0.4778157],
            [16, 0.035836177, 0.513651877],
            [17, 0.037542662, 0.551194539],
            [18, 0.049488055, 0.600682594],
            [19, 0.087030717, 0.687713311],
            [20, 0.110921502, 0.798634813],
            [21, 0.090443686, 0.889078499],
            [22, 0.066552901, 0.9556314],
            [23, 0.044368601, 1]],
            columns=['Hour', 'Hourly Profile', 'Accumulated'])

    a = random.random()
    time['Dif'] = abs(time['Accumulated']-a)

    return time['Dif'].idxmin(axis=1)


def sink(personas):
    # en mins
    avg_dur = 0.62
    stdev_dur = 0.67
    # en litros/min
    avg_flow = 4.32
    stdev_flow = 2.31

    d = []
    # 0.28 * 5.68 * 8.14 / (0.62 * 4.32) = 4.8 = 5
    while len(d) < 5 * personas:

        # Duracion
        dur = 0
        while dur < 0.01:
            dur = - avg_dur * math.log(random.random())

        # Flujo
        flu = 0
        while (flu < 1) | (flu > 11):
            flu = (avg_flow + stdev_flow * math.sin(2 * math.pi *
                                                    random.random()) *
                   math.sqrt(-2 * math.log(random.random())))

        d.append({'Hora': shower_time(), 'Duracion [min]': dur,
                  'Flujo [lts/min]': flu,
                  'Volumen [lts] caliente': dur * flu})

    df = pd.DataFrame(d)
    df['Uso'] = 'Pileta'

    return df.sort_values('Hora')


def shower(personas):
    # en mins
    avg_dur = 5.68    # 7.81 en Generator
    stdev_dur = 1.69  # 3.52 en Generator
    # en litros/min
    avg_flow = 8.14   # 8.52 en Generator
    stdev_flow = 1.76  # 2.57 en Generator

    d = []
    while len(d) < personas:

        # Duracion
        dur = 0
        while (dur < 2) | (dur > 15):
            dur = - avg_dur * math.log(random.random())

        # Flujo
        flu = 0
        while (flu < 2.75) | (flu > 11):
            flu = (avg_flow + stdev_flow * math.sin(2 * math.pi *
                                                    random.random()) *
                   math.sqrt(-2 * math.log(random.random())))

        if (flu * dur) < 120:
            d.append({'Hora': shower_time(), 'Duracion [min]': dur,
                      'Flujo [lts/min]': flu,
                      'Volumen [lts] caliente': dur * flu})

    df = pd.DataFrame(d)
    df['Uso'] = 'Ducha'

    return df.sort_values('Hora')


def DW(personas):
    # en mins
    avg_dur = 1.38    # 1.38 en Generator
    stdev_dur = 0.37  # 0.37 en Generator
    # en litros/min
    avg_flow = 5.26   # 5.26 en Generator
    stdev_flow = 0.76  # 0.76 en Generator

    d = []
    # 0.18 * 5.68 * 8.14/ (1.38 * 5.26) = 1.14 = 1
    while len(d) < personas:

        # Duracion
        dur = 0
        while dur < 0.01:
            dur = - avg_dur * math.log(random.random())

        # Flujo
        flu = 0
        while (flu < 1) | (flu > 11):
            flu = (avg_flow + stdev_flow * math.sin(2 * math.pi *
                                                    random.random()) *
                   math.sqrt(-2 * math.log(random.random())))

        d.append({'Hora': shower_time(), 'Duracion [min]': dur,
                  'Flujo [lts/min]': flu,
                  'Volumen [lts] caliente': dur * flu})
    df = pd.DataFrame(d)
    df['Uso'] = 'Platos'

    return df.sort_values('Hora')
