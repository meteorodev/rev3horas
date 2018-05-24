import util.loadConfig as lc
import util.mchConect as mch
from models import datoExtremo
import numpy as np

# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción: obtien los datos de las observaciones sinopticas

class Get3HorasData():
    """"""

    mchcred = lc.LoadConfig().getConfig("darosero")
    def __init__(self,):
        """Constructor for Get3HorasData"""


    def getDiasmes(self,año,mes):
        """devuelve el nuemro de días que debe tener un mes controlando si es bisiesto el año"""
        diasmes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if(mes==2): ##realiza la operación únicamente cuando el mes sea febrero
            if (año % 4 == 0 and año % 100 != 0 or año % 400 == 0):
                diasmes[1]=29
        return diasmes[mes-1]


    def getData(self,codigo):

        conne = mch.MchConect(self.mchcred.db_host, self.mchcred.db_user, self.mchcred.db_pass, self.mchcred.db_name)
        sentencia="select * from clm0002 where codigo ='"+codigo+"' and anio >= 2015 and anio <= 2015 and mes >= 3 and mes <= 3;"
        data = conne.pdConsulta(sentencia)


        #print(data)
        #return data

    def getTemExtSerie(self,codigo,var="tmax"):
        """devuelve los valores estremos de las temperaturas de las horas sinopticas registrados
        """
        conne = mch.MchConect(self.mchcred.db_host, self.mchcred.db_user, self.mchcred.db_pass, self.mchcred.db_name)
        sentencia = "select anio, mes , dia, "+var+" from clm0002 where codigo ='"+codigo+"';"
        data = conne.pdConsulta(sentencia)
        ##remplazar todos los valores > a 60, debido a que son inprobables

        #sin nulos
        data = data[(data[var] < 60)]
        maxtemp = data[var].max()
        mintemp = data[var].min()
        maximos = data[(data[var] == maxtemp)]
        maximos["prefi"] = "mx"
        minimos = data[(data[var] == mintemp)]
        minimos["prefi"] = "mn"
        print("maximos")
        print(maximos)
        print("minimos")
        print(minimos)

        print("Valor máximo",maxtemp,"Valor mínimo ",mintemp)
        #print(data.where(data['tmax']>60,np.nan).max(axis=0))
        print("******************datos*************************")
        print()
        return data





sinop=Get3HorasData()

extTemMax = sinop.getTemExtSerie("M0001","tmax")
extTemMin = sinop.getTemExtSerie("M0001","tmin")
sinop.getData("M0001")