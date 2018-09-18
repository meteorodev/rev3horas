# _*_ coding: utf-8 *_*
# Autor: Darwin Rosero Vaca
# Descripción: contiene las reglas para el control de calidad de datos que provienen de las libretas
# v1 24/mayo/2018 esta reglas se consideran para procesos anuales por estacion por estación
from uu import encode

import numpy as np
import pandas as pd
from time import time

from numpy.ma import append

from controller import get3horasData as d3h, getDailyData as dd
from util import enumerations as enu, toTimeSerie as ts
from models import reglasDes
from time import time

class AppReglas():
    """ definen las reglas qeu controlan la calidad de los datos
        las reglas estaran denotadas por una letra del alfabeto o
        por conbinaciones.
    """


    def __init__(self, codigo, año):
        """Constructor: Genera el dataframe con los datos de una estación dado el código y el año,
         y calcula la temperatura maxima de la serie y la minima de la serie.

         """
        self.codigo=codigo
        self.año=año
        data = d3h.Get3HorasData()
        self.data3h = data.getData(codigo, año)
        print(pd.Series(self.data3h.columns))
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
        return self.printEW(datarev," A TMAX > TMAX Serie",[0,1,2,3,4],unival=maxSerie,nameV="maxSerie",typeE=enu.TypeErros(2))

    def reglaB(self,):
        """Para ninguna observacion de la temperatura mínima
        deberá ser menor a la minima de la serie"""
        # obtener la temperatura minima de la serie
        #print(self.extTemMin[(self.extTemMin['pref'] == "mn")])
        minSerie = self.extTemMin[(self.extTemMin['pref'] == "mn")].iloc[0, 3]
        # comparar con la serire
        datarev = self.data3h[self.data3h.iloc[:, 5] <= minSerie]
        return self.printEW(datarev, " B TMIN < TMIN Serie", [0,1, 2, 3, 5], unival=minSerie, nameV="minSerie",typeE=enu.TypeErros(2))

    def reglaC(self,colIzq,colDer,regla,typeE=enu.TypeErros(1)):
        """Ninguna observacion la temmax puede ser menor a la temp de termometro seco """
        datarev = self.data3h[self.data3h.iloc[:, colIzq] <= self.data3h.iloc[:, colDer]]
        return self.printEW(datarev ,regla,[0,1,2,3,colIzq,colDer],typeE=typeE)

    def reglaD(self,colIzq,colDer,regla,typeE=enu.TypeErros(1)):
        """Ninguna observacion la tmin puede ser mayor a la tem del termometro seco a las 07 """
        datarev = self.data3h[self.data3h.iloc[:, colIzq] > self.data3h.iloc[:, colDer]]
        return self.printEW(datarev, regla, [0,1, 2, 3, colIzq, colDer],typeE= typeE)

    def reglaE(self,colIzq,colDer,regla,typeE=enu.TypeErros(1)):
        """la temperatura del termometro seco  debe ser mayor a la del termometro húmedo a las 07 """
        datarev = self.data3h[self.data3h.iloc[:, colIzq] < self.data3h.iloc[:, colDer]]
        return self.printEW(datarev, regla, [0,1, 2, 3, colIzq, colDer],typeE= typeE)


    def reglaF(self, minval=40,maxval=100):
        tsD=ts.ToTimeSerie()
        #print("\nRegla HR < 40% o HR > 100")
        """humedad relativa menor al 40% es un error"""
        #datarev = self.data3h[self.data3h.iloc[:, 9] <= 40]
        ddClass=dd.GetDailyData()
        datarev=ddClass.getDaily(self.codigo,self.año,"vd014")
        #startTime = time()
        datarevTs = tsD.unaEstacionDia(datarev)
        #elapsedTime = time() - startTime
        #print("\n appreglas.rreglaF : tiempo trasncurrido: %.10f seconds." % elapsedTime)
        #print(datarevTs)
        ltFilter=datarevTs[datarevTs['val'] <= minval].copy()

        ltFilter['causa'] = "HR <= "+str(minval)+"%"
        mtFilter=datarevTs[datarevTs['val'] >= maxval].copy()
        mtFilter['causa'] = "HR => "+str(maxval)+"%"
        datarev = pd.concat([ltFilter,mtFilter],ignore_index=True,axis=0)
        ##datarev['codigo']  =self.data3h['codigo'][0]
        """print(datarev.iloc[:,3:].max(axis=1))
        print(datarev.iloc[:, 3:].mean(axis=1))
        print(datarev.iloc[:, 3:].min(axis=1))"""

        if datarev.empty:
            return datarev
        else:
            datarev['codigo']=self.data3h['codigo'][0]
            datarev['typeE'] = enu.TypeErros(1).name
            datarev=datarev[['codigo','fecha','val','typeE','causa']]
            #print(datarev)
            #print("============================")
            return datarev


    def reglaG(self):
        """la temperatura del termometro seco  a la 13 debe ser moyor a la del termometro húmedo a las 19 """
        datarev = self.data3h[self.data3h.iloc[:, 7] < self.data3h.iloc[:, 8]]
        return self.printEW(datarev,"TS13 < TS19",[0,1,2,3,7,8],)

    def reglaH(self):
        """la temperatura del termometro seco  a la 07 debe ser menor a la del termometro húmedo a las 19 """
        datarev = self.data3h[self.data3h.iloc[:, 6] > self.data3h.iloc[:, 8]]
        return self.printEW(datarev, "TS07 > TS19", [0,1, 2, 3, 6, 8],typeE=enu.TypeErros(2))

    def reglaI(self,columna, valor, regla, typeE=enu.TypeErros(1)):
        """precipitaciones mayores a 30mm """
        datarev = self.data3h[self.data3h.iloc[:, columna] > valor]
        return self.printEW(datarev, regla, [0,1, 2, 3, columna],typeE=typeE)

    def reglaJ(self, col, valor,regla):
        """Evaporacion mayor a 5 mm """
        datarev = self.data3h[self.data3h.iloc[:, col] > valor]
        return self.printEW(datarev, regla, [0,1, 2, 3, col])

    def reglaK(self,col, valor,regla):
        """Evaporacion menor a 0 mm """
        datarev = self.data3h[self.data3h.iloc[:, col] < valor]
        return self.printEW(datarev, regla, [0,1, 2, 3, col])

    def reglaL(self):
        """Recorrido del viento a las 7 menor que el recorrido del viento siguiente"""
        print("regla para el recorrido del viento")
        #datarev = self.data3h[self.data3h.iloc[:, col] < valor]
        #return self.printEW(datarev, regla, [1, 2, 3, col])


    def printEW(self, dataf,regla,cols=[1,2,3],unival=-400,nameV="none",typeE=enu.TypeErros(1)):
        """Imprime los errores o advertencias en una tabla"""
        #print("\nRegla  " ,regla,self.data3h['codigo'][0])
        format = pd.DataFrame()
        if dataf.empty:
            #print(" No hay errores para ",varVer)
            return dataf
        else:
            dataf = dataf.iloc[:, cols].copy()
            #dataf.iloc[:, [0, 1, 2]]=dataf.iloc[:,[0,1,2]].astype(int)
            # -400 significa que se requiere crear una nueva culumna con un solo valor
            if unival != -400:
                #print("crea una columna ------")
                dataf[nameV] = unival
                dataf['typeE'] = typeE.name
                dataf['causa'] = regla
            else: #agrega la columna que se le pasa
                dataf['typeE'] = typeE.name
                dataf['causa'] = regla
            #print(dataf)
            format['codigo']=dataf['codigo']
            format['fecha']=dataf['anio'].astype(int).map(str)+"-"+dataf['mes'].astype(int).map(str)+"-"+dataf['dia'].astype(int).map(str)
            #print(dataf.columns)
            for i in range(4,len(dataf.columns)):
                va=dataf.columns[i]
                format[va]=dataf[va]
            #print(format)

        return format
