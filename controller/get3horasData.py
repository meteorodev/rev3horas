from numpy import mintypecode

import util.loadConfig as lc
import util.mchConect as mch
from models import datoExtremo
import pandas as pd
import numpy as np

# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción: obtien los datos de las observaciones sinopticas

class Get3HorasData():
    """Procesa la serie de una estación para cada año"""


    mchcred = lc.LoadConfig().getConfig("darosero")
    def __init__(self):
        """Constructor for Get3HorasData"""


    def getDiasmes(self,año,mes):
        """devuelve el nuemro de días que debe tener un mes controlando si es bisiesto el año"""
        diasmes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if(mes==2): ##realiza la operación únicamente cuando el mes sea febrero
            if (año % 4 == 0 and año % 100 != 0 or año % 400 == 0):
                diasmes[1]=29
        return diasmes[mes-1]


    def getData(self,codigo, año):
        conne = mch.MchConect(self.mchcred.db_host, self.mchcred.db_user, self.mchcred.db_pass, self.mchcred.db_name)

        """consulta los datos sin el dia 32 """
        sentencia="select * from clm0002 where codigo ='"+codigo+"' and anio = "+str(año)+" and dia < 32;"
        data = conne.pdConsulta(sentencia)
        #data.to_csv("/home/drosero/Escritorio/datates.csv",encoding="utf-8",index=False,sep=";")
        """elimina los valores de 99.9 de la columna de tmax y tmin
                    se ausme que no puede existir temperaturas mayores a 60º
                    y se remplaza esos valores por np.nan para las columnas
                    tmax  tmin  ts07  ts13  ts19  th07  th13  th19
                """
        data[(data[['tmax']] > 60)] = np.nan
        data[(data[['tmin']] > 60)] = np.nan
        data[(data[['ts07']] > 60)] = np.nan
        data[(data[['ts13']] > 60)] = np.nan
        data[(data[['ts19']] > 60)] = np.nan
        data[(data[['th07']] > 60)] = np.nan
        data[(data[['th13']] > 60)] = np.nan
        data[(data[['th19']] > 60)] = np.nan
        #data.to_csv("datatesRe.csv", encoding="utf-8", index=False, sep=";")
        return data

    def getTemExtSerie(self,codigo,var="tmax"):
        """devuelve los valores estremos de las temperaturas de las horas sinopticas registrados
        """
        conne = mch.MchConect(self.mchcred.db_host, self.mchcred.db_user, self.mchcred.db_pass, self.mchcred.db_name)
        sentencia = "select anio, mes , dia, "+var+" from clm0002 where codigo ='"+codigo+"' and dia < 32;"
        data = conne.pdConsulta(sentencia)
        data = data[(data[var] < 60)] ##devuelve los datos cuyo valor sea menor a 60 ºC
        maxtemp = data[var].max()
        mintemp = data[var].min()
        maximos = data.loc[(data[var] == maxtemp)].copy()
        maximos['pref']="mx"
        minimos = data.loc[(data[var] == mintemp)].copy()
        minimos['pref']="mn"
        return pd.concat([maximos,minimos], ignore_index=True)

    def cleanTmaxTmin(self,data3h):
        """elimina los valores de 99.9 de la columna de tmax y tmin
            se ausme qeu no puede existir temperaturas mayores a 80º
            y se remplaza esos valores por np.nan para las columnas
            tmax  tmin  ts07  ts13  ts19  th07  th13  th19
        """
        data3h[(data3h[['tmax']] > 60)] = np.nan
        data3h[(data3h[['tmin']] > 60)] = np.nan
        data3h[(data3h[['ts07']] > 60)] = np.nan
        data3h[(data3h[['ts13']] > 60)] = np.nan
        data3h[(data3h[['ts19']] > 60)] = np.nan
        data3h[(data3h[['th07']] > 60)] = np.nan
        data3h[(data3h[['th13']] > 60)] = np.nan
        data3h[(data3h[['th19']] > 60)] = np.nan
        #data3h.to_csv("/home/drosero/Escritorio/datatesRe.csv",encoding="utf-8",index=False,sep=";")





