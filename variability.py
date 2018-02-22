# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 16:39:37 2018

@author: User
"""

import pandas as pd
import matplotlib.ticker as ticker
import numpy as np
import datetime as dt


def variabilidad(runs):
    it = [3 for i in range(runs)]

    for i in range(len(it)):
        if i == 0:
            corr = anual_comparison(it[i], False)
            resE = corr[0]
            resE.rename(columns={'kWh/año': 'kWh/año ' + str(it[i]) + ' pers'}, inplace=True)
            resP = corr[1]
            resP.rename(columns={'$/año': '$/año ' + str(it[i]) + ' pers'}, inplace=True)
        else:
            corr = anual_comparison(it[i], False)
            dfE = corr[0]
            dfE.rename(columns={'kWh/año': 'kWh/año ' + str(it[i]) + ' pers'}, inplace=True)
            resE = pd.concat([resE, dfE], axis=1)
            dfP = corr[1]
            dfP.rename(columns={'$/año': '$/año ' + str(it[i]) + ' pers'}, inplace=True)
            resP = pd.concat([resP, dfP], axis=1)

    res = pd.concat([resE, resP], axis=1)
    res = res.T
    hoy = dt.date.today().strftime("%d-%m-%y")
    res.to_csv(r'generated_csvs\Resultados variabilidad ' + hoy + '.csv')
    descE = resE.T.describe()
    descP = resP.T.describe()
    desc = pd.concat([descE, descP], axis=1)
    desc.to_csv(r'generated_csvs\Describe ' + hoy + '.csv')
    varE = descE.T[['mean', 'std']]
    varE['std%'] = round(varE['std'] / varE['mean'] * 100, 2)
    varP = descP.T[['mean', 'std']]
    varP['std%'] = round(varP['std'] / varP['mean'] * 100, 2)

    return [varE, varP]


def var_integrantes():
    # consumos para 1,2,3,4 y 5 personas
    it = [i for i in range(1, 6)]

    for i in range(len(it)):
        if i == 0:
            corr = anual_comparison(it[i], False)
            resE = corr[0]
            resE.rename(columns={'kWh/año': 'kWh/año ' + str(it[i]) + ' pers'}, inplace=True)
            resP = corr[1]
            resP.rename(columns={'$/año': '$/año ' + str(it[i]) + ' pers'}, inplace=True)
        else:
            corr = anual_comparison(it[i], False)
            dfE = corr[0]
            dfE.rename(columns={'kWh/año': 'kWh/año ' + str(it[i]) + ' pers'}, inplace=True)
            resE = pd.concat([resE, dfE], axis=1)
            dfP = corr[1]
            dfP.rename(columns={'$/año': '$/año ' + str(it[i]) + ' pers'}, inplace=True)
            resP = pd.concat([resP, dfP], axis=1)

    res = pd.concat([resE, resP], axis=1)
    res = res.T

    hoy = dt.date.today().strftime("%d-%m-%y")
    res.to_csv(r'generated_csvs\Resultados distintos integ ' + hoy + '.csv')

    resE.loc[:, 'Tot'] = resE.sum(axis=1)
    resE.sort_values('Tot', ascending=False, inplace=True)
    resE.drop('Tot', axis=1, inplace=True)

    resE.plot.barh(stacked=True)
    plt.grid(False, axis='y')
    plt.xlabel('kWh/año')

    return res


def var_consumo():
    # 3 integrantes pero con consumos de -50% a +50%
    it = [3 * i / 100 for i in range(50, 160, 25)]
    labels = {it[0]: '-50 %', it[1]: '-25 %', it[2]: 'promedio',
              it[3]: '+25 %', it[4]: '+50 %'}
    for i in range(len(it)):
        if i == 0:
            corr = anual_comparison(it[i], False)
            resE = corr[0]
            resE.rename(columns={'kWh/año': 'kWh/año ' + str(labels[it[i]])}, inplace=True)
            resP = corr[1]
            resP.rename(columns={'$/año': '$/año ' + str(labels[it[i]])}, inplace=True)
        else:
            corr = anual_comparison(it[i], False)
            dfE = corr[0]
            dfE.rename(columns={'kWh/año': 'kWh/año ' + str(labels[it[i]])}, inplace=True)
            resE = pd.concat([resE, dfE], axis=1)
            dfP = corr[1]
            dfP.rename(columns={'$/año': '$/año ' + str(labels[it[i]])}, inplace=True)
            resP = pd.concat([resP, dfP], axis=1)

    res = pd.concat([resE, resP], axis=1)
    res = res.T

    hoy = dt.date.today().strftime("%d-%m-%y")
    res.to_csv(r'generated_csvs\Resultados distintos consumos ' + hoy + '.csv')

    resE.loc[:, 'Tot'] = resE.sum(axis=1)
    resE.sort_values('Tot', ascending=False, inplace=True)
    resE.drop('Tot', axis=1, inplace=True)

    resE.plot.barh(stacked=True)
    plt.grid(False, axis='y')
    plt.xlabel('kWh/año')

    return res
