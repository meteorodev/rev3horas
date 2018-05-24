# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción: CLASES MODELO, CONFIGURACIÓN DE LA BASE DE DATOS DE CONSULTA
class BaseConf():

    def __init__(self,db_host,db_user,db_pass,db_name ,db_desc,db_esta ):

        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name
        self.db_desc = db_desc
        self.db_esta = db_esta

    def toString(self):
        print(self.db_host,self.db_user,self.db_pass,self.db_name,self.db_desc,self.db_esta)

