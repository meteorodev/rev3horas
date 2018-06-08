# _*_ coding: utf-8 *_*
# Autor: Darwin Rosero Vaca
# Descripción: contiene las reglas para el contrpol de calidad de datos que provienen de las libretas
# v1 24/mayo/2018 esta reglas se consideran para procesos anuales por estacion por estación
import numpy as np
import pandas as pd
from time import time
from controller import get3horasData as d3h


class AppReglas():
    """ definen las reglas qeu controlan la calidad de los datos
        las reglas estaran denotadas por una letra del alfabeto o
        por conbinaciones.
    """

    def __init__(self, codigo, año):
        data = d3h.Get3HorasData()
        self.data3h = data.getData(codigo, año)
        self.extTemMax = data.getTemExtSerie(codigo, "tmax")
        self.extTemMin = data.getTemExtSerie(codigo, "tmin")
        """Constructor for Reglas"""


    """Reglas para temperatura"""


    def reglaA(self):
        """Para ninguna observación la temperatura maxima
        debera ser mayor a la maxima de la serie"""
        # obtener la temperatura maxima de la serie
        maxSerie = self.extTemMax[(self.extTemMax['pref'] == "mx")].iloc[0, 3]
        # comparar con la serie
        datarev = self.data3h[self.data3h.iloc[:, 4] >= maxSerie]
        return datarev

    def reglaB(self,):
        """Para ninguna observacion de la temperatura mínima
        deberá ser menor a la minima de la serie"""
        # obtener la temperatura minima de la serie
        minSerie = self.extTemMin[(self.extTemMax['pref'] == "mn")].iloc[0, 3]
        # comparar con la serire
        datarev = self.data3h[self.data3h.iloc[:, 4] >= minSerie]
        #return datarev
    def reglaC(self):
        """Ninguna observacion la temmax puede ser menor a la temp de termometro seco"""

    def reglaD(self):
        """Ninguna observacion la tmin puede ser mayor a la tem del termometro humedo"""


    def reglaE(self):
        """la temperatura del termometro seco - """

appR = AppReglas("M0003", 2014)
appR.reglaA()
