# _*_ coding: utf-8 *_*
# Autor: Darwin Rosero Vaca
# Descripción: contiene las reglas para el contrpol de calidad de datos que provienen de las libretas
# v1 24/mayo/2018 esta reglas se consideran para procesos anuales por estacion por estación
from uu import encode

import numpy as np
import pandas as pd
from time import time

from controller import get3horasData as d3h
from util import enumerations as enu
from models import reglasDes

class AppReglas():
    """ definen las reglas qeu controlan la calidad de los datos
        las reglas estaran denotadas por una letra del alfabeto o
        por conbinaciones.
    """


    def __init__(self, codigo, año):
        data = d3h.Get3HorasData()
        self.data3h = data.getData(codigo, año)
        print(self.data3h.columns)
        self.extTemMax = data.getTemExtSerie(codigo, "tmax")
        self.extTemMin = data.getTemExtSerie(codigo, "tmin")
        """Constructor for Reglas"""

    def genReglas(self):
        self.reglas=[]
        self.reglas.extend(
            [reglasDes.ReglasDes("A","La temperatura máxima no debería ser mayor a "
                                                +"la máxima de la serie","Temperatura")])
        self.reglas.extend(
            [reglasDes.ReglasDes("B", "La temperatura mínima no debería ser menor a "
                                 + "la mínima de la serie", "Temperatura")])
        self.reglas.extend(
            [reglasDes.ReglasDes("C", "Para ninguna observación la temperatura maxima debera ser menor a "
                                 + "la lectura de termometro seco", "Temperatura")])
        self.reglas.extend(
            [reglasDes.ReglasDes("D", "Para ninguna observación la temperatura mínima debera ser mayor a "
                                 + "la lectura de termometro seco", "Temperatura")])
        self.reglas.extend(
            [reglasDes.ReglasDes("E", "La lectura del termometro seco debe ser mayor a  "
                                 + "la lectura de termometro húmedo", "Temperatura")])

    """Reglas para temperatura"""


    def reglaA(self):
        """Para ninguna observación la temperatura maxima
        debera ser mayor a la maxima de la serie"""
        # obtener la temperatura maxima de la serie
        #print(self.extTemMax[(self.extTemMax['pref'] == "mx")])
        maxSerie = self.extTemMax[(self.extTemMax['pref'] == "mx")].iloc[0, 3]
        # comparar con la serie
        datarev = self.data3h[self.data3h.iloc[:, 4] >= maxSerie]
        return self.printEW(datarev,"TMAX > TMAX Serie",[1,2,3,4],maxSerie,"maxSerie",enu.TypeErros(2))

    def reglaB(self,):
        """Para ninguna observacion de la temperatura mínima
        deberá ser menor a la minima de la serie"""
        # obtener la temperatura minima de la serie
        #print(self.extTemMin[(self.extTemMin['pref'] == "mn")])
        minSerie = self.extTemMin[(self.extTemMin['pref'] == "mn")].iloc[0, 3]
        # comparar con la serire
        datarev = self.data3h[self.data3h.iloc[:, 5] <= minSerie]
        return self.printEW(datarev, "TMIN < TMIN Serie", [1, 2, 3, 5], minSerie, "minSerie",enu.TypeErros(2))

    def reglaC07(self):
        """Ninguna observacion la temmax puede ser menor a la temp de termometro seco a las 07 """
        datarev = self.data3h[self.data3h.iloc[:, 4] <= self.data3h.iloc[:, 6]]
        rev =self.printEW(datarev ,"TMAX > TS07",[1,2,3,4,6],typeE=enu.TypeErros(1))
    def reglaC13(self):
        """Ninguna observacion la temmax puede ser menor a la temp de termometro seco a las 13 """
        datarev  = self.data3h[self.data3h.iloc[:, 4] < self.data3h.iloc[:, 7]]
        rev =self.printEW(datarev ,"TMAX >= TS13",[1,2,3,4,7],typeE=enu.TypeErros(1))
    def reglaC19(self):
        """Ninguna observacion la temmax puede ser menor a la temp de termometro seco a las 19 """
        datarev  = self.data3h[self.data3h.iloc[:, 4] <= self.data3h.iloc[:, 8]]
        rev =self.printEW(datarev ,"TMAX > TS19",[1,2,3,4,8],typeE=enu.TypeErros(1))


    def reglaD07(self):
        """Ninguna observacion la tmin puede ser mayor a la tem del termometro seco a las 07"""
        datarev = self.data3h[self.data3h.iloc[:, 5] > self.data3h.iloc[:, 6]]
        return self.printEW(datarev, "TMNM <= TS07", [1, 2, 3, 5, 6], typeE=enu.TypeErros(1))
    def reglaD13(self):
        """Ninguna observacion la tmin puede ser mayor a la tem del termometro seco a las 13"""
        datarev = self.data3h[self.data3h.iloc[:, 5] >= self.data3h.iloc[:, 7]]
        return self.printEW(datarev, "TMNM < TS13", [1, 2, 3, 5, 7], typeE=enu.TypeErros(1))
    def reglaD19(self):
        """Ninguna observacion la tmin puede ser mayor a la tem del termometro seco a las 19"""
        datarev = self.data3h[self.data3h.iloc[:, 5] >= self.data3h.iloc[:, 8]]
        return self.printEW(datarev, "TMNM < TS19", [1, 2, 3, 5, 8], typeE=enu.TypeErros(1))

    def reglaE07(self):
        """la temperatura del termometro seco  debe ser mayor a la del termometro húmedo a las 07 """
        datarev = self.data3h[self.data3h.iloc[:, 6] < self.data3h.iloc[:, 9]]
        return self.printEW(datarev, "TS07 > TH07", [1, 2, 3, 6, 9], typeE=enu.TypeErros(1))
    def reglaE13(self):
        """la temperatura del termometro seco  debe ser mayor a la del termometro húmedo a las 13 """
        datarev = self.data3h[self.data3h.iloc[:, 7] < self.data3h.iloc[:, 10]]
        return self.printEW(datarev, "TS13 > TH13", [1, 2, 3, 7, 10], typeE=enu.TypeErros(1))
    def reglaE19(self):
        """la temperatura del termometro seco  debe ser mayor a la del termometro húmedo a las 19 """
        datarev = self.data3h[self.data3h.iloc[:, 8] < self.data3h.iloc[:, 11]]
        return self.printEW(datarev, "TS19 > TH19", [1, 2, 3, 8, 11], typeE=enu.TypeErros(1))

    def reglaF(self):
        """humedad relativa menor al 40% es un error"""


    def printEW(self, dataf,varVer,cols=[1,2,3],unival=-400,nameV="none",typeE=enu.TypeErros(1)):
        """Imprime los errores o advertencias en un a tabla"""
        print("\nRegla  " ,varVer)
        if dataf.empty:
            #print(" No hay errores para ",varVer)
            return 5000
        else:
            dataf = dataf.iloc[:, cols].copy()
            dataf.iloc[:, [0, 1, 2]]=dataf.iloc[:,[0,1,2]].astype(int)
            # -400 significa que se requiere crea una nueva culumna con un solo valor
            if unival != -400:
                dataf[nameV] = unival
                dataf['typeE'] = typeE.name
            else: #agrega la columna que se le pasa
                dataf['typeE'] = typeE.name
            print(dataf)
            return dataf


appR = AppReglas("M0003", 2014)

ra=appR.reglaA()
#appR.printEW(ra)
rb=appR.reglaB()
#appR.printEW(rb)
rc07=appR.reglaC07()
rc13=appR.reglaC13()
rc19=appR.reglaC19()
rd07=appR.reglaD07()
rd13=appR.reglaD13()
rd19=appR.reglaD19()
re07=appR.reglaE07()
re13=appR.reglaE13()
re19=appR.reglaE19()
