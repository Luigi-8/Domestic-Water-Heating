# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 15:53:22 2018

@author: User
"""
import pandas as pd
import numpy as np

# SYSTEMS

Tsal = 60   # Temp salida

def calefon(base, Efi, colector=False):
    if Efi == 'A':
        EE = 75     # Min para que sea A es 75%
    elif Efi == 'B':
        EE = 68     # Min para que sea B es 68%
    elif Efi == 'C':
        EE = 61     # Min para que sea C es 61%

    Cn = 60     # Min recomendado por UTE es 60 lts
    Qpr = (5.815 * Cn) / EE - 0.05815 * Cn       # en kWh/día
    # Se supone eficiencia de conversion de la resistencia = 1

    key = 'Tmains'
    if colector:
        key = 'Temp salida a respaldo'

    base['Econs [kWh]'] = Qpr / 24 + base['Total lts caliente'] * 4.184 * (Tsal - base[key]) / 3600

    return base.loc[:, ['DOY', 'MES', 'Hora', 'Econs [kWh]']]


def bbacalor(base, colector=False):

    # COP de paper con DT entre Tamb y adentro del calentador
    # 0.74 kWh/día para el de argas de 20 a 45 grados
    Qpr = 0.74 / 25 * (60 - 18)
    base['COP'] = 6.81 - 0.121 * (Tsal - base['TAM']) + 0.00063 * (Tsal - base['TAM']) * (Tsal - base['TAM'])

    key = 'Tmains'
    if colector:
        key = 'Temp salida a respaldo'

    base['Econs [kWh]'] = Qpr / 24 + base['Total lts caliente'] * 4.184 * (Tsal - base[key]) / (base['COP'] * 3600)

    return base.loc[:, ['DOY', 'MES', 'Hora', 'Econs [kWh]']]


def gas_almacen(base, colector=False,  EF=0.67):
    # EF tiene en cuenta perdidas ya que es energia util que sale / total de energia entregada al calentador
    # EF minimo para que cumpla con certificacion Energy Star 0.67 para menores de 208 lts

    key = 'Tmains'
    if colector:
        key = 'Temp salida a respaldo'

    base['Econs [kWh]'] = base['Total lts caliente'] * 4.184 * (Tsal - base[key]) / (EF * 3600)

    return base.loc[:, ['DOY', 'MES', 'Hora', 'Econs [kWh]']]


def gas_inst(base, colector=False, EF=0.9):
    # EF tiene en cuenta perdidas ya que es energia util que sale / total de energia entregada al calentador
    # EF minimo para que cumpla con certificacion Energy Star 0.9

    key = 'Tmains'
    if colector:
        key = 'Temp salida a respaldo'

    base['Econs [kWh]'] = base['Total lts caliente'] * 4.184 * (Tsal - base[key]) / (EF * 3600)

    return base.loc[:, ['DOY', 'MES', 'Hora', 'Econs [kWh]']]

# TARIFFS
# ELECTRICITY


def resdoble(df):
    punta = 8.157
    llano = 3.267
    df.loc[(df['Hora'] > 16) & (df['Hora'] < 23), 'Precio $/kWh'] = punta
    df.loc[df['Hora'] < 17, 'Precio $/kWh'] = llano
    df.loc[df['Hora'] == 23, 'Precio $/kWh'] = llano
    df['$'] = df['Precio $/kWh'] * df['Econs [kWh]']

    return df.groupby(by=['MES'])['$'].agg(np.sum).reset_index()


def ressimple(df):
    # Etotal en kWh
    pivot = df.groupby(by=['MES'])['Econs [kWh]'].agg(np.sum).reset_index()
    # Segun UTE 37% de la energia consumida es para calentamient de agua
    for i in range(len(pivot)):
        pivot.loc[i, '$'] = (p_ressim(pivot.loc[i, 'Econs [kWh]'] / 0.37) - p_ressim(pivot.loc[i, 'Econs [kWh]'] / 0.37 * 0.63))

    # pivot.loc[df['Etotal']<101,'$']= df['Etotal']*hasta100
    # pivot.loc[(df['Etotal']>101) & (df['Etotal']<601),'$']= (df['Etotal'] - 100)*hasta600 + 100*hasta100
    # pivot.loc[df['Etotal']>601,'$']= (df['Etotal'] - 600)*mas600 + 100*hasta100 + 500*hasta600

    return pivot.loc[:, ['MES', '$']]


def p_ressim(value):
    hasta100 = 4.881
    hasta600 = 6.121
    mas600 = 7.63

    if value > 600:
        return (value - 600) * mas600 + 100 * hasta100 + 500 * hasta600
    elif value > 100:
        return 100 * hasta100 + (value - 100) * hasta600
    else:
        return value * hasta100


def basica(df):
    # Etotal en kWh
    pivot = df.groupby(by=['MES'])['Econs [kWh]'].agg(np.sum).reset_index()
    # meses con mas de 230 kWh
    mesesmasde230 = pivot[pivot['Econs [kWh]'] > 230].gropuby(['MES'])['Econs [kWh]'].count()

    hasta100 = 295.8
    hasta140 = 6.092
    hasta350 = 11.139
    mas350 = 7.393
    pivot.loc[df['Econs [kWh]'] < 101, '$'] = hasta100
    pivot.loc[(df['Econs [kWh]'] > 101) & (df['Econs [kWh]'] < 140), '$'] = (df['Econs [kWh]'] - 101) * hasta140 + hasta100
    pivot.loc[(df['Econs [kWh]'] > 140) & (df['Econs [kWh]'] < 350), '$'] = (df['Econs [kWh]'] - 140) * hasta350 + hasta100 + 40 * hasta140
    pivot.loc[df['Econs [kWh]'] > 350, '$'] = (df['Econs [kWh]'] - 350) * mas350 + hasta100 + 110 * hasta350 + 40 * hasta140

    return pivot.loc[:, ['MES', '$']]

# GAS


def gasres(df):
    # Precio por m3 N Mde gas 28.05 Conecta canelones 22.319
    precio = 29.98
    # 9300 kcal/m3 N
    PCI = 9300 * 4.184 / 3600
    # PCI en kWh / m3
    df = df.groupby(by=['MES'])['Econs [kWh]'].agg(np.sum).reset_index()
    df['$'] = df['Econs [kWh]'] / PCI * precio

    return df.loc[:, ['MES', '$']]


def supergas(df):
    # Precio por kg es 37.8
    precio = 43.5
    # 11.800 Kcal/kg
    PCI = 11800 * 4.184 / 3600
    # PCI en kWh / kg
    df = df.groupby(by=['MES'])['Econs [kWh]'].agg(np.sum).reset_index()
    df['$'] = df['Econs [kWh]'] / PCI * precio

    return df.loc[:, ['MES', '$']]
