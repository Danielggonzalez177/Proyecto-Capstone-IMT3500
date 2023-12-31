import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Test_Logicos import test_logico
from Test_Distribuciones import test_distribuciones
from Test_Isolation import test_isolation
from Test_Series import test_series
from alarma_1 import alarma_1
from alarma_2 import alarma_2
from alarma_3 import alarma_3
from time import time


################
## PARAMETROS ##
################

# Parametros de lectura de Datos
PATH_TEST_DICC = "..\E01_T_DEU_CONS_2303_REV.csv"
PATH_2210 = "..\E01_T_DEU_CONS_2210_REV.csv"
PATH_2211 = "..\E01_T_DEU_CONS_2211_REV.csv"
PATH_2212 = "..\E01_T_DEU_CONS_2212_REV.csv"
PATH_2301 = "..\E01_T_DEU_CONS_2301_REV.csv"
PATH_2302 = "..\E01_T_DEU_CONS_2302_REV.csv"
PREV_DICCS = ["..\E01_T_DEU_CONS_2210_REV.csv",
              "..\E01_T_DEU_CONS_2211_REV.csv",
              "..\E01_T_DEU_CONS_2212_REV.csv",
              "..\E01_T_DEU_CONS_2301_REV.csv",
              "..\E01_T_DEU_CONS_2302_REV.csv"]

PATH_DICC = "..\DownloadAll\Diccionario T_DEU_CONS.xlsx"

# Diccionarios auxiliares
DICC_CODFAM = list(pd.read_excel(PATH_DICC, sheet_name='CODFAM')['CODIGO'])[1:]
DICC_CODTLP = list(pd.read_excel(PATH_DICC, sheet_name='CODTLP')['CODIGO'])
DICC_PROD = list(pd.read_excel(PATH_DICC, sheet_name='CODPRO')['CODIGO'])[1:]

# A futuro definimos esto segun columnas
umbral = {'R': 5, 'Y': 10}

# Codigos de banco, moneda y estado aceptados (basado en dicc de datos)
BANCO_CODS = [39,27]
MONEDA_CODS = [1,2,3]
ESTADO_CODS = [1,2,3,4]

# Archivos a escribir
FILENAME_LOGICOS = "logic_results.csv"
FILENAME_DIST = "dist_results.csv"
FILENAME_ISOLATION = "isolation_results.csv"
FILENAME_SERIES = "series_results.csv"

# Codigos logicos
CODIGOS = {"BANCO_CODS": BANCO_CODS,
           "MONEDA_CODS": MONEDA_CODS,
           "DICC_CODFAM": DICC_CODFAM,
           "DICC_CODTLP": DICC_CODTLP,
           "DICC_PROD": DICC_PROD,
           "ESTADO_CODS":ESTADO_CODS,
           "umbral":umbral}

# Columnas a usar para tests de distribuciones
COLUMNAS_DIST = ["MTOREV", "SALMD", "GASTO", "ULTXCO", "MTOVENC", \
                 "TASAINT", "SPROM", "MTOCAST", "CONTINGENTE"]
SIGNIFICANCIA = 0.05 # alpha

# Durbin-Watson
umbral_DW = 0.95
CODIGOS_SERIES = {
    "MIN_DW": 1.72789, # Basado en tablas DW
    "MAX_DW": 1.80942, # Basado en tablas DW
    "COLUMNAS_DW": ["DIASMORA"],
    "UMBRAL_DW": umbral_DW}

# Columnas a usar para tests de Isolation Forest
COLUMNAS_ISOLATION = ['ESTADO', 'MTOINT', 'MTOORIG', 'MTOORIGP',
       'MONEDA', 'MTOVENC', 'DCOMO2', 'DCOMO3', 'MTOCAST', 'DIASMORA',
       'MTOREV',  'TASAINT', 'FECOPE',
       'FECVEN', 'SALDOPUNTA','MCUOTA', 'SPROM']
# Parametros extra de iForest
CONTAMINACION = 0.1
N_ESTIMATORS = 100
SHOW_PCA = False # True si se quiere visualizar resultados iForest con reduc. dim.

# Umbrales para etapas estadisticas yiForest, respectivamente
UMBRAL_ALARMA_2 = 0.7
UMBRAL_ALARMA_3 = 0.7

#####################
## INICIO DE TESTS ##
#####################

print("INICIO TESTEO")
while(True):
    # Tests logicos 
    print('Iniciando Tests Logicos')
    t1 = time()
    resultados_logicos = test_logico(FILENAME_LOGICOS,PATH_TEST_DICC,PATH_DICC,CODIGOS)
    t2 = time()
    print(f'Tests Logicos finalizados\nTiempo: {t2-t1:.2f} s')

    # Alarma Logicos
    if not alarma_1(resultados_logicos):
        print("Se levanta la alarma 1. No se pasaron los tests logicos")
        #break

    # Tests de distribuciones
    print('Iniciando Tests Distribuciones')
    t3 = time()
    resultados_distribuciones = test_distribuciones(FILENAME_DIST,PATH_TEST_DICC,PREV_DICCS[-1],COLUMNAS_DIST,SIGNIFICANCIA)
    t4 = time()
    print(f'Tests Distribuciones finalizados\nTiempo: {t4-t3:.2f} s')
    
    # Tests de Series
    print('Iniciando Tests Series')
    t5 = time()
    resultados_series = test_series(FILENAME_SERIES,PATH_TEST_DICC,PREV_DICCS,CODIGOS_SERIES)
    t6 = time()
    print(f'Tests Series finalizados\nTiempo: {t6-t5:.2f} s')

    # Alarma Estadisticos
    if not alarma_2(resultados_distribuciones,resultados_series,UMBRAL_ALARMA_2):
        print("Se levanta la alarma 2. No se pasaron los tests estadisticos")
        break
    
    # Tests de iForest
    print('Iniciando Tests IForest')
    t7 = time()
    resultados_isolation = test_isolation(PATH_TEST_DICC,CONTAMINACION,FILENAME_ISOLATION,COLUMNAS_ISOLATION,N_ESTIMATORS,SHOW_PCA)
    t8 = time()
    print(f'Tests IForest finalizados\nTiempo: {t8-t7:.2f} s')

    # Alarma iForest
    if not alarma_3(resultados_isolation,UMBRAL_ALARMA_3):
        print("Se levanta la alarma 2. No se pasaron los tests de ML")
        break

    print(f'Todos los tests pasados! Base de datos {PATH_TEST_DICC} correcta.')
    break

print("FIN TESTEO")