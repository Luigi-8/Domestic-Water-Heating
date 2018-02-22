# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 16:31:42 2018

@author: User
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import datetime as dt


def economia(personas=0):
    anual_comp = anual_comparison(personas)

    npv_rate = 0.1
    inv = {'cal': 8369, 'bomba': 34800, 'G_al': 15600, 'G_in': 17703,
           'Col': 49590}
    # Mant Esc. Base es 0
    mant = {'cal': 0, 'bomba': 1000, 'G_al': 2020, 'G_in': 2020, 'Col': 1000}
    df = anual_comp[1].copy()
    df['Ahorro'] = df.loc['Esc. Base', '$/año'] - df['$/año']
    df.reset_index(inplace=True)

    df = df.loc[df['Sistema'] != 'Esc. Base', :]
    zipped = zip(['Inv', 'Mant'], [inv, mant])
    for i, j in zipped:
        df.loc[:, i] = 0
        df.loc[df['Sistema'].str.contains('Calefón'), i] = j['cal']
        df.loc[df['Sistema'].str.contains('Bomba'), i] = j['bomba']
        df.loc[df['Sistema'].str.contains('Alm'), i] = j['G_al']
        df.loc[df['Sistema'].str.contains('Inst'), i] = j['G_in']
        df.loc[df['Sistema'].str.contains('con cole'), i] += j['Col']

    df['PRS'] = round((df['Inv'] / (df['Ahorro'] - df['Mant'])), 1)
    for k in range(1, len(df)+1):
        # 10 anos se toma como vida util
        flujo = [(df.loc[k, 'Ahorro'] - df.loc[k, 'Mant'])
                 for i in range(10 + 1)]
        flujo[0] = -df.loc[k, 'Inv']
        df.loc[k, 'IRR'] = round(np.irr(flujo) * 100, 0)
        df.loc[k, 'NPV'] = round(np.npv(npv_rate, flujo), 0)

    df.set_index('Sistema', inplace=True)
    df.sort_values('PRS', inplace=True)

    hoy = dt.date.today().strftime("%d-%m-%y")
    df.to_csv(r'generated_csvs\Resultados economicos ' + hoy + '.csv')

    plt.figure()
    ax1 = plt.subplot(121)
    plt.barh(range(len(df)), df['PRS'], align='center')
    plt.yticks(range(len(df)), df.index, fontsize=20)
    plt.xlabel('años', fontsize=24)
    plt.xticks(fontsize=20)
    ax1.set_axisbelow(True)
    plt.grid(False, axis='y')
    plt.title('Payback Simple', fontsize=28, color='c')
    rects = ax1.patches
    # esp = 0.35 * rects[-1].get_width()
    for rect, label in zip(rects, df.PRS):
        width = rect.get_width()
        ax1.text(width * 0.8, rect.get_y(), label, ha='center', va='bottom',
                 fontsize=18, color='w', weight='bold')

    ax2 = plt.subplot(122, sharey=ax1)
    plt.barh(range(len(df)), df['IRR'], align='center', color='r')
    plt.xlabel('%', fontsize=24)
    plt.xticks(fontsize=20)
    ax2.set_axisbelow(True)
    plt.grid(False, axis='y')
    plt.setp(ax2.get_yticklabels(), visible=False)
    plt.title('Tasa Interna de Retorno', fontsize=28, color='c')
    rects = ax2.patches
    for rect, label in zip(rects, df.IRR.astype(int)):
        width = rect.get_width()
        ax2.text(width * 0.8, rect.get_y(), label, ha='center', va='bottom',
                 fontsize=18, color='w', weight='bold')

    plt.subplots_adjust(wspace=0, left=0.18)

    plt.figure()
    ax = plt.subplot(111)
    ord_NPV = df.NPV.sort_values(ascending=False).astype(int)
    plt.barh(range(len(ord_NPV)), ord_NPV, align='center')
    plt.yticks(range(len(ord_NPV)), ord_NPV.index, fontsize=20)
    plt.xlabel('miles de $', fontsize=24)
    plt.xticks(fontsize=20)
    ax1.set_axisbelow(True)
    plt.grid(False, axis='y')
    plt.title('NPV', fontsize=28, color='c')
    rects = ax1.patches
    # esp = 0.35 * rects[-1].get_width()
#==============================================================================
#     for rect, label in zip(rects, ord_NPV):
#         width = rect.get_width()
#         ax.text(width * 0.8, rect.get_y(), label, ha='center', va='bottom', fontsize=18, color='r', weight='bold')
#
#==============================================================================
    scale_x = 1000
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
    ax.xaxis.set_major_formatter(ticks_x)

    return df
