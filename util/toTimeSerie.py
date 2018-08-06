# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción:
from _tracemalloc import start
from builtins import type, filter

import pandas as pd
import numpy as np
from time import time


class ToTimeSerie():
    """Esta clase transforma un amatrix a tipo serie de datos en formato año mes dia valor"""

    def __init__(self,):
        """Constructor for ToTimeSerie"""

    def unaEstacionDia(self, datam):
        """Tranfoema la matriz de datos diarios a timeserie
        del formato : codigo    anio   mes    v1    v2  ...    v27   v28   v29   v30   v31
        al formato  codigo    anio   mes dia valor
        """
        print("Con funcion iloc")
        firstR = datam.iloc[1,:]
        codigo=firstR.iloc[0]
        ai=int(firstR.iloc[1])
        mesi=1
        lastR = datam.iloc[-1, :]
        af = int(firstR.iloc[1])
        mesf=12
        # crea la serie con las fechas
        serie=pd.date_range((str(ai)+"/01/01"),(str(af)+"/12/31"),name="fecha").to_frame(index=False)
        serie["val"]=np.nan
        print(serie.head())
        #se recorre cada fila del dataframe de datos y se calcula la posicion basado en el dia que ocupe
        posi=0
        posf=0
        cuentadias=0
        while ai <= af:
            while mesi <= mesf:
                dmes=self.getDiasmes(ai,mesi)
                posf+=dmes
                #filtrar los datos po r las fechas en las que se va recorriendo
                filtrado=datam[(datam['anio']==ai) & (datam['mes']==mesi)]
                if filtrado.empty == False:
                    print("fecha inicial ", ai, "-", mesi, " fecha final ", af, "-", mesf, "dias a contar ", dmes,
                          "conteo ", str(cuentadias))
                    serie.iloc[posi:posf,1] = filtrado.iloc[0,3:(dmes+3)].values
                mesi+=1
                posi=posf
            mesi=1
            ai+=1
        print(serie)



    def añoAdias(self,ad):
        # comprueba si es biciesto
        if (ad % 4 == 0 and ad % 100 != 0 or ad % 400 == 0):
            dias = 366
        else:
            dias =  365
        return dias


    def calculaPos(self,ai,aa,mi,ma,di,da):
        """Calcula la posiscionj que deve ocupar el en vector dado como parametros

        ai=año de inicio , aa = año actual(leido de los datos)
        mi=mes de inicio , ma = mes actual(leido de los datos)
        di=dia de inicio , ma = dia actual(leido de los datos)
        """
        fa=aa-ai
        fm=ma-mi
        fd=da-di




    def getDiasmes(self,año,mes):
        """devuelve el nuemro de días que debe tener un mes controlando si es bisiesto el año"""
        diasmes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if(mes==2): ##realiza la operación únicamente cuando el mes sea febrero
            if (año % 4 == 0 and año % 100 != 0 or año % 400 == 0):
                diasmes[1]=29
        return diasmes[mes-1]
