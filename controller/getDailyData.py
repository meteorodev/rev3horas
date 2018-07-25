# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción:
from pandas.plotting import table

import util.loadConfig as lc
import util.mchConect as mch
import pandas as pd
import numpy as np

class GetDailyData():
    """Obtiene los datos deiarios en base al nombre de las tablas por variable,
        se requiere conocer el nombre de la tabla de datos diarios
    """
    mchcred = lc.LoadConfig().getConfig("darosero")
    def __init__(self,):
        """Constructor for GetDailyData"""

    def getDaily(self,codigo, año,tabla):
        conne = mch.MchConect(self.mchcred.db_host, self.mchcred.db_user, self.mchcred.db_pass, self.mchcred.db_name)

        """consulta los datos sin el dia 32 """
        sentencia = "select * from "+tabla+" where codigo ='" + codigo + "' and anio = " + str(año) + ";"
        data = conne.pdConsulta(sentencia)
        # data.to_csv("/home/drosero/Escritorio/datates.csv",encoding="utf-8",index=False,sep=";")
        """elimina los valores de 99.9 de la columna de tmax y tmin
                    se ausme que no puede existir temperaturas mayores a 60º
                    y se remplaza esos valores por np.nan para las columnas
                    tmax  tmin  ts07  ts13  ts19  th07  th13  th19
                """

        # data.to_csv("datatesRe.csv", encoding="utf-8", index=False, sep=";")
        return data
