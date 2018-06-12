# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción:

class ReglasDes():
    """Clase Reglas en la cual se describen las reglas utilizadas para manejarles en los reportes"""


    def __init__(self,codigo,descripcion,variable):
        """Constructor for ReglasDes"""
        self.codigo=codigo;
        self.descripcion=descripcion
        self.variable=variable

    def to_string(self):
        print(self.codigo," : ",self.descripcion," : aplicable a ",self.variable)