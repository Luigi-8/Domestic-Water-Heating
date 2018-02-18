# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 16:28:18 2018

@author: User
"""

import pandas as pd
import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import style
import matplotlib.ticker as ticker
import datetime as dt


def anual_comparison(personas=0):
    yeardata = gen_yeardata(personas)
    for b in range(1, 3):
        for a in range(1, 3):
            if b == 2 and a == 1:
                continue
            key = {1: 'DOY', 2: 'MES'}          # parametro a
            key2 = {1: 'Econs [kWh]', 2: '$'}   # parametro b
            tit = {1: 'Calefón A ', 2: 'Bomba de calor ', 3: 'Gas con Alm. ', 4: 'Gas Inst. '}

            if b == 1:
                es_base = calefon(yeardata, 'B').groupby([key[a]])[key2[b]].sum().reset_index()
                es_caleA = calefon(yeardata, 'A').groupby([key[a]])[key2[b]].sum().reset_index()
                es_caleA_col = calefon(yeardata, 'A', True).groupby([key[a]])[key2[b]].sum().reset_index()
                es_bba = bbacalor(yeardata).groupby([key[a]])[key2[b]].sum().reset_index()
                es_bba_col = bbacalor(yeardata, True).groupby([key[a]])[key2[b]].sum().reset_index()
                es_gasal = gas_almacen(yeardata).groupby([key[a]])[key2[b]].sum().reset_index()
                es_gasal_col = gas_almacen(yeardata, True).groupby([key[a]])[key2[b]].sum().reset_index()
                es_gasin = gas_inst(yeardata).groupby([key[a]])[key2[b]].sum().reset_index()
                es_gasin_col = gas_inst(yeardata, True).groupby([key[a]])[key2[b]].sum().reset_index()
                esc = {1: es_caleA, 2: es_bba, 3: es_gasal, 4: es_gasin}
                esc3 = {1: es_caleA_col, 2: es_bba_col, 3: es_gasal_col, 4: es_gasin_col}
                labels = {1: '', 2: '', 3: '', 4: ''}
                ylab = 'Consumo kWh/día'
                if a == 2:
                    ylab = 'Consumo kWh/mes'
                    totalE = {'Esc. Base': es_base[key2[b]].sum(),
                              tit[1]: esc[1][key2[b]].sum(),
                              tit[2]: esc[2][key2[b]].sum(),
                              tit[3]: esc[3][key2[b]].sum(),
                              tit[4]: esc[4][key2[b]].sum(),
                              tit[1] + ' con Col.': esc3[1][key2[b]].sum(),
                              tit[2] + ' con Col.': esc3[2][key2[b]].sum(),
                              tit[3] + ' con Col.': esc3[3][key2[b]].sum(),
                              tit[4] + ' con Col.': esc3[4][key2[b]].sum()}

            else:
                ylab = 'Consumo $/mes'
                tar = {1: ressimple, 2: resdoble, 3: gasres, 4: supergas}
                es_base = ressimple(calefon(yeardata, 'B'))
                es_caleA_rs = tar[1](calefon(yeardata, 'A'))
                es_caleA_rs_col = tar[1](calefon(yeardata, 'A', True))
                es_caleA_dh = tar[2](calefon(yeardata, 'A'))
                es_caleA_dh_col = tar[2](calefon(yeardata, 'A', True))
                es_bba_rs = tar[1](bbacalor(yeardata))
                es_bba_rs_col = tar[1](bbacalor(yeardata, True))
                es_bba_dh = tar[2](bbacalor(yeardata))
                es_bba_dh_col = tar[2](bbacalor(yeardata, True))
                es_gasal_gn = tar[3](gas_almacen(yeardata))
                es_gasal_gn_col = tar[3](gas_almacen(yeardata, True))
                es_gasal_glp = tar[4](gas_almacen(yeardata))
                es_gasal_glp_col = tar[4](gas_almacen(yeardata, True))
                es_gasin_gn = tar[3](gas_inst(yeardata))
                es_gasin_gn_col = tar[3](gas_inst(yeardata, True))
                es_gasin_glp = tar[4](gas_inst(yeardata))
                es_gasin_glp_col = tar[4](gas_inst(yeardata, True))
                esc = {1: es_caleA_rs, 2: es_bba_rs, 3: es_gasal_gn, 4: es_gasin_gn}
                esc2 = {1: es_caleA_dh, 2: es_bba_dh, 3: es_gasal_glp, 4: es_gasin_glp}
                esc3 = {1: es_caleA_rs_col, 2: es_bba_rs_col, 3: es_gasal_gn_col, 4: es_gasin_gn_col}
                esc4 = {1: es_caleA_dh_col, 2: es_bba_dh_col, 3: es_gasal_glp_col, 4: es_gasin_glp_col}
                labels = {1: 'Res. Simp.', 2: 'Res. Simp.', 3: 'Gas Nat.', 4: 'Gas Nat.'}
                labels2 = {1: 'Doble Hor.', 2: 'Doble Hor.', 3: 'GLP', 4: 'GLP'}
                totalP = {'Esc. Base': es_base[key2[b]].sum(),
                          tit[1] + labels[1]: esc[1][key2[b]].sum(),
                          tit[2] + labels[2]: esc[2][key2[b]].sum(),
                          tit[3] + labels[3]: esc[3][key2[b]].sum(),
                          tit[4] + labels[4]: esc[4][key2[b]].sum(),
                          tit[1] + labels2[1]: esc2[1][key2[b]].sum(),
                          tit[2] + labels2[2]: esc2[2][key2[b]].sum(),
                          tit[3] + labels2[3]: esc2[3][key2[b]].sum(),
                          tit[4] + labels2[4]: esc2[4][key2[b]].sum(),
                          tit[1] + 'con colect ' + labels[1]: esc3[1][key2[b]].sum(),
                          tit[2] + 'con colect ' + labels[2]: esc3[2][key2[b]].sum(),
                          tit[3] + 'con colect ' + labels[3]: esc3[3][key2[b]].sum(),
                          tit[4] + 'con colect ' + labels[4]: esc3[4][key2[b]].sum(),
                          tit[1] + 'con colect ' + labels2[1]: esc4[1][key2[b]].sum(),
                          tit[2] + 'con colect ' + labels2[2]: esc4[2][key2[b]].sum(),
                          tit[3] + 'con colect ' + labels2[3]: esc4[3][key2[b]].sum(),
                          tit[4] + 'con colect ' + labels2[4]: esc4[4][key2[b]].sum()}

            plt.figure()
            style.use('fivethirtyeight')

            maxy = int(round(es_base[key2[b]].max() * 1.3))
            y = [i for i in range(0, maxy, round(maxy/5))]
                               
            ax1 = plt.subplot(4, 1, 1)
            ax2 = plt.subplot(4, 1, 2)
            ax3 = plt.subplot(4, 1, 3)
            ax4 = plt.subplot(4, 1, 4)
                        
            ax = {1: ax1, 2: ax2, 3: ax3, 4: ax4}
            for i in range(1, 5):
                if i == 1:
                    ax[i] = plt.subplot(4, 1, 1)
                else:
                    ax[i] = plt.subplot(4, 1, i, sharex=ax1)
                plt.plot(es_base[key[a]], es_base[key2[b]], label='Esc. Base', color='r', linewidth=1.5)
                plt.plot(esc[i][key[a]], esc[i][key2[b]], label=labels[i] + ' sin colector', color='b', linewidth=1.5)
                plt.plot(esc3[i][key[a]], esc3[i][key2[b]], label=labels[i] + ' con colector', color='tab:orange', linewidth=1.5)

                if b == 2:
                    plt.plot(esc2[i][key[a]], esc2[i][key2[b]], label=labels2[i] + ' sin colector', color='m', linewidth=1.5)
                    plt.plot(esc4[i][key[a]], esc4[i][key2[b]], label=labels2[i] + ' con colector', color='tab:gray', linewidth=1.5)
                    plt.fill_between(es_base[key[a]], es_base[key2[b]], esc2[i][key2[b]], where=(es_base[key2[b]] > esc2[i][key2[b]]), color='g', alpha=0.2)
                    plt.fill_between(es_base[key[a]], esc2[i][key2[b]], es_base[key2[b]], where=(es_base[key2[b]] < esc2[i][key2[b]]), color='y', alpha=0.2)

                plt.fill_between(es_base[key[a]], es_base[key2[b]], esc[i][key2[b]], where=(es_base[key2[b]] > esc[i][key2[b]]), color='g', alpha=0.2)
                plt.fill_between(es_base[key[a]], esc[i][key2[b]], es_base[key2[b]], where=(es_base[key2[b]] < esc[i][key2[b]]), color='y', alpha=0.2)
                if i == 3:
                    plt.ylabel(ylab, fontsize=24)
                plt.yticks(y, fontsize=20)
                plt.ylim(-maxy*0.03, maxy)
                plt.legend(fontsize=10, loc=2)
                plt.setp(ax[i].get_xticklabels(), visible=False)
                plt.grid(True)
                plt.title('Esc. ' + tit[i], fontsize=28, color='c')
                if i == 4:
                    plt.setp(ax[i].get_xticklabels(), visible=True)
                    x = [i for i in range(1, 13)]
                    plt.xlabel("Mes del año", fontsize=24)
                    if a == 1:
                        x = [i for i in range(15, 366, 15)]
                        x.insert(0, 1)
                        plt.xlabel("día del año", fontsize=24)
                    plt.xticks(x, fontsize=20)

            plt.subplots_adjust(hspace=0.15)

    plt.figure()
    ax = plt.subplot(1, 1, 1)
    plt.title('Consumo calentamiento de agua caliente anual', fontsize=28, color='c')
    ordenadaE = pd.DataFrame(totalE, index=['kWh/año']).transpose().sort_values(by='kWh/año', ascending=False)
    plt.barh(range(len(ordenadaE)), ordenadaE.iloc[:, 0], align='center')
    plt.yticks(range(len(ordenadaE)), ordenadaE.index, fontsize=20)
    plt.xlabel('kWh / año', fontsize=24)
    plt.xticks(fontsize=20)
    ax.set_axisbelow(True)
    plt.grid(False, axis='y')
    porc = [int((i / ordenadaE.at['Esc. Base', 'kWh/año'])* 100) for i in ordenadaE.values]
    labels = [str(i) + '% del Esc. Base' for i in porc ]
    rects = ax.patches
    # esp = 0.3 *rects[-1].get_width()
    for rect, label in zip(rects, labels):
        width = rect.get_width()
        ax.text(width * 0.8, rect.get_y(), label, ha='center', va='bottom', fontsize=20, color='r', weight='bold')
    # rect.get_y() + rect.get_height()/2
    
    plt.figure()
    ax = plt.subplot(1, 1, 1)
    plt.title('Costo calentamiento de agua caliente anual', fontsize=28, color='c')
    ordenadaP = pd.DataFrame(totalP, index=['$/año']).transpose().sort_values(by='$/año', ascending=False)
    plt.barh(range(len(ordenadaP)), ordenadaP.iloc[:, 0], align='center')
    plt.yticks(range(len(ordenadaP)), ordenadaP.index, fontsize=20)
    plt.xlabel('miles de $ / año', fontsize=24)
    plt.xticks(fontsize=20)
    ax.set_axisbelow(True)
    plt.grid(False, axis='y')
    porc = [int((i / ordenadaP.at['Esc. Base', '$/año'])* 100) for i in ordenadaP.values]
    labels = [str(i) + '% del Esc. Base' for i in porc ]
    rects = ax.patches
    # esp = 0.35 * rects[-1].get_width()
    for rect, label in zip(rects, labels):
        width = rect.get_width()
        ax.text(width * 0.9, rect.get_y(), label, ha='center', va='bottom', fontsize=18, color='r', weight='bold')
    
    scale_x = 1000
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
    ax.xaxis.set_major_formatter(ticks_x)
    plt.subplots_adjust(left=0.18)

    # ordenadaP['Sistema'] = ordenadaP.index
    ordenadaP.index.name = 'Sistema'
    ordenadaE.index.name = 'Sistema'
    # ordenadaP = ordenadaP.reset_index()
    # ordenadaP = ordenadaP[['Sistema', '$/año']]
    ordenadaP = ordenadaP.round(0)
    ordenadaE = ordenadaE.round(0)

    hoy = dt.date.today().strftime("%d-%m-%y")
    ordenadaE.to_csv(r'generated_csvs\Consumo anual Energia ' + hoy + '.csv')
    ordenadaP.to_csv(r'generated_csvs\Costo anual ' + hoy + '.csv')

    return [ordenadaE, ordenadaP]
