import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Test_Logicos import test_logico






# Seccion previa a los tests


PATH_TEST_DICC = "Datos\E01_T_DEU_CONS_2303.csv"

PATH_2210 = "Datos\E01_T_DEU_CONS_2210.csv"
PATH_2211 = "Datos\E01_T_DEU_CONS_2211.csv"
PATH_2212 = "Datos\E01_T_DEU_CONS_2212.csv"
PATH_2301 = "Datos\E01_T_DEU_CONS_2301.csv"
PATH_2302 = "Datos\E01_T_DEU_CONS_2302.csv"



PATH_DICC = "Datos\Diccionario T_DEU_CONS.xlsx"



DICC_CODFAM = list(pd.read_excel(PATH_DICC, sheet_name='CODFAM')['CODIGO'])[1:]
DICC_CODTLP = list(pd.read_excel(PATH_DICC, sheet_name='CODTLP')['CODIGO'])
DICC_PROD = list(pd.read_excel(PATH_DICC, sheet_name='CODPRO')['CODIGO'])[1:]

# A futuro definimos esto segun columnas
umbral = {'R': 5, 'Y': 10}



BANCO_CODS = [39,27]
MONEDA_CODS = [1,2,3]
FILENAME = "logic_results.csv"
CODIGOS = {"BANCO_CODS":BANCO_CODS,
           "MONEDA_CODS":MONEDA_CODS,
           "DICC_CODFAM":DICC_CODFAM,
           "DICC_CODTLP":DICC_CODTLP,
           "DICC_PROD":DICC_PROD,
           "umbral":umbral}


# Tests logicos 



resultados_logicos = test_logico(FILENAME,PATH_TEST_DICC,CODIGOS)




# Tests de distribuciones




