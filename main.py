import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Test_Logicos import test_logico
from Test_Distribuciones import test_distribuciones
from alarma_1 import alarma_1




# Seccion previa a los tests


PATH_TEST_DICC = "..\DownloadAll\E01_T_DEU_CONS_2303\E01_T_DEU_CONS_2303.csv"

PATH_2210 = "..\DownloadAll\E01_T_DEU_CONS_2210\E01_T_DEU_CONS_2210.csv"
PATH_2211 = "..\DownloadAll\E01_T_DEU_CONS_2211\E01_T_DEU_CONS_2211.csv"
PATH_2212 = "..\DownloadAll\E01_T_DEU_CONS_2212\E01_T_DEU_CONS_2212.csv"
PATH_2301 = "..\DownloadAll\E01_T_DEU_CONS_2301\E01_T_DEU_CONS_2301.csv"
PATH_2302 = "..\DownloadAll\E01_T_DEU_CONS_2302\E01_T_DEU_CONS_2302.csv"
PREV_DICCS = ["...\E01_T_DEU_CONS_2210.csv",
              "...\E01_T_DEU_CONS_2211.csv",
              "...\E01_T_DEU_CONS_2212.csv",
              "...\E01_T_DEU_CONS_2301.csv",
              "...\E01_T_DEU_CONS_2302.csv"]


PATH_DICC = "..\DownloadAll\Diccionario T_DEU_CONS.xlsx"



DICC_CODFAM = list(pd.read_excel(PATH_DICC, sheet_name='CODFAM')['CODIGO'])[1:]
DICC_CODTLP = list(pd.read_excel(PATH_DICC, sheet_name='CODTLP')['CODIGO'])
DICC_PROD = list(pd.read_excel(PATH_DICC, sheet_name='CODPRO')['CODIGO'])[1:]

# A futuro definimos esto segun columnas
umbral = {'R': 5, 'Y': 10}



BANCO_CODS = [39,27]
MONEDA_CODS = [1,2,3]
FILENAME_LOGICOS = "logic_results.csv"
FILENAME_DIST = "logic_results.csv"
CODIGOS = {"BANCO_CODS":BANCO_CODS,
           "MONEDA_CODS":MONEDA_CODS,
           "DICC_CODFAM":DICC_CODFAM,
           "DICC_CODTLP":DICC_CODTLP,
           "DICC_PROD":DICC_PROD,
           "umbral":umbral}
COLUMNAS_DIST = ["MTOREV","SALMD","GASTO","ULTXCO","MTOVENC", "TASAINT","SPROM","MTOCAST","CONTINGENTE"]
SIGNIFICANCIA = 0.05
# Tests logicos 

while(True):


    resultados_logicos = test_logico(FILENAME_LOGICOS,PATH_TEST_DICC,PATH_DICC,CODIGOS)


# Levantamos la alarma 
    if not alarma_1(resultados_logicos):
        break


# Tests de distribuciones

    resultados_distribuciones = test_distribuciones(FILENAME_DIST,PATH_TEST_DICC,PREV_DICCS[-1],COLUMNAS_DIST,SIGNIFICANCIA)
    



