from controller.appReglas import AppReglas
from util import enumerations as enu
from openpyxl import Workbook

#Estaciones selecionadas

listEstation=['M1219','M1221','M1230','M1231','M1233','M1238','M1239','M1240','M1243','M1244','M1246','M1248',
    'M1249','M1250','M1256','M1257','M1257','M1259','M1260','M1261','M1265','M1267']


wb= Workbook()

ws=wb.active

for est in listEstation:
    appR = AppReglas(est, 2014)
    ra=appR.reglaA()
    rb=appR.reglaB()
    rc07=appR.reglaC(colIzq=4,colDer=6,regla="Tmx > Ts a las 07")
    rc13=appR.reglaC(colIzq=4,colDer=7,regla="Tmx > Ts a las 13")
    rc19=appR.reglaC(colIzq=4,colDer=8,regla="Tmx > Ts a las 19")
    rd07=appR.reglaD(colIzq=5,colDer=6,regla="Tmn <= Ts a las 07")
    rd13=appR.reglaD(colIzq=5,colDer=7,regla="Tmn <= Ts a las 13")
    rd19=appR.reglaD(colIzq=5,colDer=8,regla="Tmn <= Ts a las 19")
    re07=appR.reglaE(colIzq=6,colDer=9,regla="TS07 < TH07")
    re13=appR.reglaE(colIzq=7,colDer=10,regla="TS13 < TH13")
    re19=appR.reglaE(colIzq=8,colDer=11,regla="TS19 < TH19")
    rf=appR.reglaF()
    rg=appR.reglaG()
    rh=appR.reglaH()
    ri07=appR.reglaI(12,30,"RR > 30 mm a las 07",enu.TypeErros(2))
    ri13=appR.reglaI(13,30,"RR > 30 mm a las 13 ",enu.TypeErros(2))
    ri19=appR.reglaI(14,30,"RR > 30 mm a las 19 ",enu.TypeErros(2))
    """rj07=appR.reglaJ(15,5,"Evap > 5 m a las 07")
    rj13=appR.reglaJ(17,5,"Evap > 5 m a las 13")
    rj19=appR.reglaJ(19,5,"Evap > 5 m a las 19")
    rk07=appR.reglaK(19,0,"Evap < 0 m a las 07")
    rk13=appR.reglaK(19,0,"Evap < 0 m a las 13")
    rk19=appR.reglaK(19,0,"Evap < 0 m a las 19")
    """
    frames=[ra,rb,rc07,rc13,rc19,rd07,rd13,rd19,re07,re13,re19,rf,rg,rh,ri07,ri13,ri19]

    for df in frames:
        if not df.empty:
            #print("en el for")
            #print(df)
            #print("fin del for")
            for rowdf in range(0,len(df)):
                print(df.iloc[rowdf, :].values)
                ws.append(list(df.iloc[rowdf,:].values))
            
wb.save("/home/drosero/Escritorio/anuario2014.xlsx")