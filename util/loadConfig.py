# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción: lee la configuración generada een la base inicial que esta dentro de sqlite3
from models import baseConf as db
import sqlite3
import os

class LoadConfig():
    """"""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self):
        """Constructor vacio"""

    def getConfig(self,user):
        base=os.path.join(self.BASE_DIR, 'db.sqlite3')

        con_bd = sqlite3.connect(base)
        cursor=con_bd.cursor()
        cursor.execute('SELECT type,name,sql,tbl_name FROM `main`.sqlite_master;')
        tablas = cursor.fetchone()  # retrieve the first row
        if tablas is None:
            print("La base esta vacia")
        else:
            sent='select * from base_consulta_baseconf where db_user="'+user+'";'
            #print(sent)
            cursor.execute(sent)
            lh=cursor.fetchone()
            bc=db.BaseConf(lh[1],lh[2],lh[3],lh[4],lh[5],lh[6])
        cursor.close()
        return bc

        #print(user1[0])  # Print the first column retrieved(user's name)

