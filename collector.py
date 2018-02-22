# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 15:38:45 2018

@author: User
"""

import math
import pandas as pd


def collector(base):

    Tseteo = 60

    # TK almacenamiento
    capTK = 150     # litros
    emis = 0.075    # acero inox pulido
    Rext = 0.585/2 - 0.05
    espaisl = 0.05
    kaisl = 0.04    # lana de vidrio y PUF
    Raisl = Rext + espaisl
    largo = 0.981        # del cilindro
    Aext = 2 * math.pi * Raisl * largo  # Aext del cilindro del tanque

    # Collector
    n0 = 0.7
    FRUL = 2
    A = 2.33       # Aperture Area

    # canos a sistema de respaldo
    Rext_ca = 0.0213 / 2    # canos usados
    espaisl_ca = 0.024      # 5cm de espesor
    Raisl_ca = Rext_ca + espaisl_ca
    emis_ca = 0.93
    kaisl_ca = 0.03

    base['Ttk'] = 0
    base['Qu'] = 0
    base['lts salen TK'] = 0
    base['Temp salida a respaldo'] = 0
    # base['Ef inst'] = 0

    cols = base.columns.tolist()

    cal = cols.index('Total lts caliente')
    TAM = cols.index('TAM')
    Tmains = cols.index('Tmains')
    Vviento = cols.index('VVI10')
    GTI45 = cols.index('GTI45')

    Ttk = cols.index('Ttk')
    Qu = cols.index('Qu')
    Vsale = cols.index('lts salen TK')
    Tsale = cols.index('Temp salida a respaldo')
    # Ef = cols.index('Ef inst')

    # z para ajustar vel del viento de 10 a 3 m de altura, para ciudades es 0.7
    z = 0.7

    base.iloc[0, Ttk] = 60  # base.iloc[0, Tmains]

    for i in range(1, len(base)):
        tm = base.iloc[i - 1, Ttk]
        ta = base.iloc[i, TAM]
        G = base.iloc[i, GTI45]
        Qutil = A * (G * n0 - FRUL * (tm - ta))
        if Qutil > 0:
            base.iloc[i, Qu] = Qutil
            # base.iloc[i, Ef] = n0 - FRUL * (tm - ta) / G
        else:
            base.iloc[i, Qu] = 0

        # Perdidas en la caneria
        Tp = 50
        Tp1 = 20
        while True:
            # z para ajustar vel del viento de 10 m a 3 m de altura
            hc = (5.7 + 3.8 * (math.log(3 / z) / math.log(10 / z)) *
                  base.iloc[i, Vviento])
            hr = (emis_ca * 5.67E-8 * (((Tp + 273) ** 4 - (ta + 273) ** 4)) /
                  (Tp - ta))
            h = hr + hc
            # Qp/L de canos considero temp tk o 60 si es mayor Ttk
            Qpcan = (2 * math.pi * (min(tm, Tseteo) - ta) / (math.log(Raisl_ca / Rext_ca) / kaisl_ca + 1 / (h * Raisl_ca)))
            Tp1 = Qpcan / (h * math.pi * 2 * Raisl_ca) + ta

            if int(Tp) == int(Tp1):
                break
            else:
                Tp = (Tp + Tp1) / 2

        # 10 metros de canos, 1000 J / kJ, 4.182 kJ / kg C, 0.067 l/s (4 l/min)
        perdidas = Qpcan * 10 / 1000 / 4.182 / 0.067

        # Temp a respaldo y volumen retirado del TK
        tmains = base.iloc[i, Tmains]
        if tm < (Tseteo + perdidas):
            base.iloc[i, Tsale] = tm - perdidas
            base.iloc[i, Vsale] = base.iloc[i, cal]
        else:
            base.iloc[i, Tsale] = Tseteo
            base.iloc[i, Vsale] = (base.iloc[i, cal] *
                                   (Tseteo + perdidas - tmains) / (tm - tmains))
        # Perdidas en el cuerpo del TK
        Tpc = 50
        Tp1c = 20
        while True:
            hc = (5.7 + 3.8 * (math.log(3 / z) / math.log(10 / z)) *
                  base.iloc[i, Vviento])
            hr = (emis * 5.67E-8 * (((Tpc + 273) ** 4 - (ta + 273) ** 4)) /
                  (Tpc - ta))
            h = hr + hc
            # Qp del cilindro
            Qpc = (2 * math.pi * largo * (tm - ta) /
                   (math.log(Raisl / Rext) / kaisl + 1 / (h * Raisl)))

            Tp1c = Qpc / (h * Aext) + ta
            if int(Tpc) == int(Tp1c):
                break
            else:
                Tpc = (Tpc + Tp1c) / 2

        # Perdidas en las tapas del TK
        Tpt = 50
        Tp1t = 20
        while True:
            hc = (5.7 + 3.8 * (math.log(3 / z) / math.log(10 / z)) *
                  base.iloc[i, Vviento])
            hr = (emis * 5.67E-8 * (((Tpt + 273) ** 4 - (ta + 273) ** 4)) /
                  (Tpt - ta))
            h = hr + hc
            # Qp de una tapa
            Qpt = math.pi * Raisl ** 2 * (tm - ta) / (espaisl / kaisl + 1 / h)

            Tp1t = Qpt / (h * math.pi * Raisl ** 2) + ta
            if int(Tpt) == int(Tp1t):
                break
            else:
                Tpt = (Tpt + Tp1t) / 2

        Qp = Qpc + 2 * Qpt
        # Qu y Qp en Wh por lo que multiplico x 3600 y / 1000 para KJ
        base.iloc[i, Ttk] = (tm + (base.iloc[i, Qu] * 3.6 - Qp * 3.6 -
                 base.iloc[i, Vsale] * 4.182 * (tm - tmains)) / (capTK * 4.182))

    return base
