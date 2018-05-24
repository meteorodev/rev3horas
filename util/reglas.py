# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción: contiene las reglas para el contrpol de calidad de datos que provienen de las libretas
#v1 24/mayo/2018 esta reglas se consideran para procesos mensuales por estación

class Reglas():
    """ definen las reglas qeu controlan la calidad de los datos
        las reglas estaran denotadas por una letra del alfabeto o por conbinaciones.
    """

    def __init__(self,):
        """Constructor for Reglas"""
    def reglaA(self,serie, maxdeSerie):
        """Para ninguna observación la temperatura maxima
        debera ser mayor a la maxima de la serie"""

