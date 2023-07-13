import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def to_float(s):
    if type(s) != float:
        s = str(s).split(",")
        if len(s) == 1 or not s[-1].isdigit():
            return float(f"{int(s[0])}.0")
        elif not s[0].isdigit() and s[-1].isdigit():
            return float(f"0.{int(s[-1])}")
        return float(f"{int(s[0])}.{int(s[-1])}")
    return s

def formato(df,PATH_DICC):
    'Retorna alarmas si columnas de la df estan en mal formato: (formato actual, formato en diccionario)'

    dfdic = pd.read_excel(PATH_DICC, \
                        sheet_name='T_DEU_CONS')[['Column_name', 'Type', 'Length']]
    dt = df.dtypes

    alertas = []
    for i in dfdic.index:

        if ('int' in dfdic['Type'][i]) and (dt[dfdic['Column_name'][i]] == np.int64):
            pass # formato correcto
        elif ('char' in dfdic['Type'][i]) and (dt[dfdic['Column_name'][i]] == str):
            pass # formato correcto
        elif ('char' in dfdic['Type'][i]) and (dt[dfdic['Column_name'][i]] == object):
            pass # formato correcto (Consideramos validos char como objetos)
        elif ('float' in dfdic['Type'][i]) and (dt[dfdic['Column_name'][i]] == float):
            pass # formato correcto
        elif ('decimal' in dfdic['Type'][i]) and (dt[dfdic['Column_name'][i]] == float):
            pass # formato correcto
        else:
            alertas.append(f'ALERTA ({dfdic["Column_name"][i]}): ({dt[dfdic["Column_name"][i]]}, {dfdic["Type"][i]})')

    return alertas


def duplicidad_id_mov(df, umbral = 5):
    'Revisa si el indice unico (Rut, NUMOPE) es unico, y retorna si cumple o no y el porcentaje de error'
    df1 = df.groupby(['RUT', 'NUMOPE']).size().reset_index(name='Size')
    num = int(df1[df1.Size > 1].shape[0])
    den = int(df.shape[0])
    
    if 100*(num/den) > umbral:
        return "No cumple", 100*(num/den)
    return "Cumple", 100*(num/den)




def duplicidad_num_cuenta(df, umbral = 5):
    'Revisa si hay duplicados, y retorna si cumple o no y el porcentaje de error'
    df1 = df.loc[:, ['RUT', 'NUMOPE']]
    Ob = df1.duplicated().value_counts()
    op_duplicadas = Ob[True]
    den = int(df.shape[0])
    if op_duplicadas == 0:
        return "Cumple",0
    return "No cumple",100*(op_duplicadas/den)

def fechas_validas(df, umbral = 5):
    'Revisa si los dias en FECOPE estan en formato correcto, y retorna si cumple o no y el porcentaje de error'
    cantidad = df[~df.FECOPE.isna()].FECOPE.apply(lambda x: int(str(x)[-4:-2]) > 31).value_counts()
    prc = 100*(1-cantidad[False]/df[~df.FECOPE.isna()].shape[0])
    if prc > umbral:
        return "No cumple", prc
    return "Cumple", prc



#8 EXACTITUD PARA INTERES
def exactitud_intereses(df, umbral = 5):
    'Revisa la proporcion de NaN en TASAINT, y retorna si cumple o no y el porcentaje de error'
    if df.TASAINT.dtype == float:
        a = "formato correcto"
    else:
        a="formato incorrecto"
    num = int(df.TASAINT.shape[0])
    den = int(df.TASAINT.isna().sum())
    if 100*(den/num) > umbral:
        return "No cumple", 100*(den/num)
    return "Cumple", 100*(den/num)


# Test de MTOREV 15/16
def test_mtorev(df,to_float, umbral = 5):
    'Revisa si MTOREV toma valores 0, y retorna si cumple o no y el porcentaje de error'
    n = df.shape[0]
    if df.MTOREV.dtype == float:
        prc = 100*df[df.MTOREV == 0].shape[0]/n
    else:
        df['MTOREVf'] = df.MTOREV.apply(to_float)
        prc = 100*df[df.MTOREVf == 0].shape[0]/n
    if prc > umbral:
            return ("No cumple", prc)
    return ("Cumple",prc)
    

def test_estado(df,ESTADO_CODS):
    'Revisa si estado esta dentro de los valores definidos, y retorna si cumple o no y el porcentaje de error'
    count = len(df) - len(df[(df["ESTADO"].isin(ESTADO_CODS))])
    if count > 0:
        return "No Cumple", 100*(count/len(df))
    else:
        return "Cumple",0


def cod_banco(df,codigos_banc_val):
    'Revisa que el codigo de banco este entre los valores definidos, y retorna si cumple o no y el porcentaje de error'
    if   df["BANCO"].isin(codigos_banc_val).all():
        return "Cumple",0
    
    return "No cumple",100*(len(df["BANCO"].isin(codigos_banc_val))/len(df))





def cod_divisa(dataframe,codigos_moneda_val):
    'Verificar que las monedas esten dentro de las definidas'
    if   dataframe["MONEDA"].isin(codigos_moneda_val).all():
        return "Cumple",0
    
    return "No cumple",100*(len(dataframe[(dataframe["MONEDA"].isin(codigos_moneda_val))]))/(len(dataframe))




def cod_producto(dataframe,DICC_PROD, umbral = 5):
    'Verifica que CODPRO este dentro de los valores definidos'
    count = dataframe[~dataframe.CODPRO.isin(DICC_PROD)].shape[0]
    if count/dataframe.shape[0] > umbral:
        return "No cumple", 100*count/dataframe.shape[0]
    return "Cumple", 0



def cod_tlp(dataframe,DICC_CODTLP, umbral = 5):
    'Verificar que CODTLP este dentro de los valores especificados'
    count = dataframe[~dataframe.CODPRO.isin(DICC_CODTLP)].shape[0]
    if count/dataframe.shape[0] > umbral:
        return "No cumple", 100*count/dataframe.shape[0]
    return "Cumple", 0




def DIASMORA0_ESTADO1(df, umbral = 5):
    'Test (DIASMORA0_ESTADO1): Revisar que si DIASMORA es 0, entonces ESTADO = 1'
    
    # Numero de filas con DIASMORA = 0
    n = df[df.DIASMORA == 0].shape[0]

    # Si los dias de mora son 0, las cuotas deberian estar vigentes (solo estado 1)
    distr = df[(df.DIASMORA == 0)].ESTADO.value_counts()
    prc = (1 - distr[1]/n)*100
    
    if prc > umbral:
        return ('No cumple', round(prc,2))
    return ('Cumple', round(prc,2))




def DIASMORA30_ESTADO2(df, umbral = 5):
    '''Test (DIASMORA30_ESTADO2):  
    Si los dias de mora son < 30 y > 0, entonces solo debemos obtener estado: 2 (0 < mora < 30 dias)'''

    # Numero de filas con DIASMORA > 0 y < 30
    n = df[(df.DIASMORA < 30) & (df.DIASMORA > 0)].shape[0]

    # Si los dias de mora son < 30, las cuotas deberian estar en mora 1 (solo estado 2)
    distr = df[(df.DIASMORA < 30) & (df.DIASMORA > 0)].ESTADO.value_counts()
    prc = (1 - distr[[1,2]].sum()/n)*100
    
    if prc > umbral:
        return ('No cumple', round(prc,2))
    return ('Cumple', round(prc,2))


def DIASMORA89_ESTADO5(df, umbral = 5):
    '''Test (DIASMORA89_ESTADO5):  
    Si los dias de mora son <= 89 y >= 30, entonces solo debemos obtener estado: 5'''

    # Numero de filas con DIASMORA >= 30 y <= 89
    n = df[(df.DIASMORA >= 30) & (df.DIASMORA <= 89)].shape[0]

    #  Si los dias de mora son (<= 89 y >= 30), entonces solo debemos obtener estado: 5
    distr = df[(df.DIASMORA >= 30) & (df.DIASMORA <= 89)].ESTADO.value_counts()
    prc = (1 - distr[5]/n)*100
    
    if prc > umbral:
        return ('No cumple', round(prc,2))
    return ('Cumple', round(prc,2))




def fec_movimiento(df, umbral = 5):
    'Revisa los NaN en las fechas, y retorna si cumple o no y el porcentaje de error'
    if df.FECOPE.dtype == int:
        a = "formato correcto"
    else:
        a="formato incorrecto"
    num1 = int(df.TASAINT.shape[0])
    den1 = int(df.TASAINT.isna().sum())

    if 100*(den1/num1) > umbral:
        return "No cumple", 100*(den1/num1)
    return "Cumple", 100*(den1/num1)


def test_results(df,PATH_DICC,CODIGOS):
    'Ejecuta los tests anteriores'

    tests = pd.DataFrame(columns=['Test', 'Resultado'])
    tests.loc[len(tests)] = ['Formato', formato(df,PATH_DICC)]
    tests.loc[len(tests)] = ['duplicidad_id_mov', duplicidad_id_mov(df)]
    tests.loc[len(tests)] = ['duplicidad_num_cuenta', duplicidad_num_cuenta(df)]
    tests.loc[len(tests)] = ['fechas_validas', fechas_validas(df)]
    tests.loc[len(tests)] = ['fec_movimiento', fec_movimiento(df)]
    tests.loc[len(tests)] = ['exactitud_intereses', exactitud_intereses(df)]
    tests.loc[len(tests)] = ['test_mtorev', test_mtorev(df,to_float)]
    tests.loc[len(tests)] = ['test_estado', test_estado(df,CODIGOS["ESTADO_CODS"])]
    tests.loc[len(tests)] = ['cod_banco', cod_banco(df,CODIGOS["BANCO_CODS"])]
    tests.loc[len(tests)] = ['cod_divisa', cod_divisa(df,CODIGOS["MONEDA_CODS"])]
    tests.loc[len(tests)] = ['cod_producto', cod_producto(df,CODIGOS["DICC_PROD"])]
    tests.loc[len(tests)] = ['cod_tlp', cod_tlp(df,CODIGOS["DICC_CODTLP"])]
    tests.loc[len(tests)] = ['DIASMORA0_ESTADO1', DIASMORA0_ESTADO1(df)]
    tests.loc[len(tests)] = ['DIASMORA30_ESTADO2', DIASMORA30_ESTADO2(df)]
    tests.loc[len(tests)] = ['DIASMORA89_ESTADO5', DIASMORA89_ESTADO5(df)]
    

    return tests


def test_logico(FILENAME,PATH_DICC_TEST,PATH_DICC,CODIGOS):
    "Escribe los resultados en FILENAME.csv"
    df = pd.read_csv(PATH_DICC_TEST,delimiter=";")
    tests = test_results(df,PATH_DICC,CODIGOS)

    tests.to_csv(FILENAME, index=False)


    return tests

