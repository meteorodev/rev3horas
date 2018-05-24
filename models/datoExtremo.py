# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción:

class DatoExtremo():
    """Clase modelo para datos extemos, maimos o minimos """


    def __init__(self,año,mes,dia,valorx,prefijo):
        """Constructor for DatoExtremo"""
        self.año = año
        self.mes = mes
        self.dia = dia
        self.valorx = valorx
        self.prefijo = prefijo
        #self.valorm = valorm
        ##self.unidades=unidades
        ##self.variable=variable

    def toString(self):

        print("año",self.año,"mes:",self.mes,"dia:",self.dia,"valor",self.valor,"prefijo",self.prefijo)