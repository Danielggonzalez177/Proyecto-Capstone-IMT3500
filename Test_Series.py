import numpy as np
import pandas as pd
from statsmodels.stats.stattools import durbin_watson
import math
from scipy.stats import norm
#Cambiar el path *Importante
PATH_2210 = "E01_T_DEU_CONS_2210_REV.csv"
PATH_2211 = "E01_T_DEU_CONS_2211_REV.csv"
PATH_2212 = "E01_T_DEU_CONS_2212_REV.csv"
PATH_2301 = "E01_T_DEU_CONS_2301_REV.csv"
PATH_2302 = "E01_T_DEU_CONS_2302_REV.csv"
PATH_2303 = "E01_T_DEU_CONS_2303_REV.csv"
Lista_Path = [PATH_2210,PATH_2211,PATH_2212,PATH_2301,PATH_2302,PATH_2303]

def RutComunes(lista):
    dataframelist = []
    for i in lista:
        df = pd.read_csv(i, delimiter=";", usecols = ['RUT'])
        dataframelist.append(df)

    interseccion = np.array(dataframelist[0]['RUT'])

    for df in dataframelist[1:]:
        RutComunes = np.intersect1d(interseccion, df['RUT'])
        
    dfRutComunes = pd.DataFrame({'RUT': RutComunes})
    lista_rut = dfRutComunes["RUT"]
    return lista_rut

def Data(df):
    cantidad_filas = df.shape[0]
    tamaño_muestra =calcular_tamano_muestra(cantidad_filas,0.05,0.5,0.05)
    lista_dataframes =[]
    for i in range (1000):
        dataframe_muestra = df.sample(tamaño_muestra)
        lista_dataframes.append(dataframe_muestra)

    num_columnas = lista_dataframes[0].shape[1]
    a = 1
    nuevas_fechas = {i: str(a + i) for i in range(num_columnas-1)}
    lista_fechas = list(nuevas_fechas.values())
    lista_durbinwatson = []
    for j in lista_dataframes:
        lista_durbinwatsonfecha = []
        for fecha in lista_fechas:
            if int(fecha) != len(lista_fechas):
                dw_test = TestSeriesDW(j,int(fecha),int(fecha)+1)
            lista_durbinwatsonfecha.append(dw_test)
        lista_durbinwatson.append(lista_durbinwatsonfecha)
    lista_final = []

    for lista in lista_durbinwatson:
        nueva_lista = lista[:-1] 
        lista_final.append(nueva_lista)
    return lista_final



def TestSeriesDW (df,fecha_1,fecha_2):

    df_fecha_1 = df[str(fecha_1)]
    df_fecha_2 = df[str(fecha_2)]
    dw_test = durbin_watson(df_fecha_2 - df_fecha_1)
    return dw_test


def calcular_tamano_muestra(N, alpha, p, d):
    z = abs(norm.ppf(1 - alpha/2)) 
    numerator = (N * z**2 * p * (1 - p))
    denominator = (d**2 * (N - 1) + z**2 * p * (1 - p))
    n = numerator / denominator
    muestra_tamaño = math.ceil(n)
    return muestra_tamaño

def Test(Variable,lista,valor_maximo,valor_minimo,umbral):
    lista_rut=RutComunes(lista)
    dataframelist = []
    dataframelistna = []
    for i in lista:
        df1 = pd.read_csv(i, delimiter=";", usecols = ['RUT',Variable])
        df2 = df1.loc[df1['RUT'].isin(lista_rut)].dropna()
        dataframelist.append(df1)
        dataframelistna.append(df2)
    
    
    dataframes=[]
    a=1
    for i in dataframelistna:
        tupla = (i,str(a))
        dataframes.append(tupla)
        a += 1
    dftemporal = pd.DataFrame()
   
    
    for df, nombre_df in dataframes:
        dftemporal[nombre_df] = df[Variable]

    dftemporal['RUT'] = dataframelist[0]['RUT'] 
    dftemporal = dftemporal.dropna()

    
    dataframeDW = Data(dftemporal)
    Matrix = np.array(dataframeDW)
    mayores = np.mean(Matrix >= valor_maximo) * 100
    menores = np.mean(Matrix <= valor_minimo) * 100
    media = np.mean((Matrix >= valor_minimo) & (Matrix <= valor_maximo)) * 100

    #print("Porcentaje de elementos donde no existe evidencia de autocorrelación positiva: ", mayores)
    #print("Porcentaje de elementos donde existe evidencia de autocorrelación positiva: ", menores)
    #print("Porcentaje de elementos no concluyentes:", media)

    NewMatrix =  np.abs(Matrix - 4)

    may = np.mean(NewMatrix>= valor_maximo) * 100
    men = np.mean(NewMatrix <= valor_minimo) * 100
    med = np.mean((NewMatrix >= valor_minimo) & (NewMatrix <= valor_maximo)) * 100
    #print("Porcentaje de elementos donde no existe evidencia de autocorrelación negativa: ", may)
    #print("Porcentaje de elementos donde existe evidencia de autocorrelación negativa: ", men)
    #print("Porcentaje de elementos no concluyentes:", med)
    if (menores >= umbral or may >= umbral) or (med >= umbral and  media >= umbral):
        return ["Cumple",mayores,menores,media,may,men,med]
    return ["No cumple",mayores,menores,media,may,men,med]



def test_series(FILENAME_SERIES,PATH_TEST_DICC,PREV_DICCS,CODIGOS_SERIES):
    Lista_Path = PREV_DICCS
    Lista_Path.append(PATH_TEST_DICC)
    tests = pd.DataFrame(columns=['Test', 'Resultado'])
    COLUMNAS_TEST = CODIGOS_SERIES["COLUMNAS_DW"]
    for i in range(len(COLUMNAS_TEST)):
        tests.loc[len(tests)] = [f"DW_{COLUMNAS_TEST[i]}",Test(COLUMNAS_TEST[i],Lista_Path,CODIGOS_SERIES["MAX_DW"],CODIGOS_SERIES["MIN_DW"],CODIGOS_SERIES["UMBRAL_DW"])]
    tests.to_csv(FILENAME_SERIES,index=False)
    return tests
