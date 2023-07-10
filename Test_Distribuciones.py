import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.stats as stat
from scipy.stats import kstest, mannwhitneyu



def df_dropna(DataFrame,por=0):
    return DataFrame.dropna()


def df_fillna_mean(Dataframe,por=0):
    return Dataframe.fillna(value = Dataframe.mean())


def df_fillna_normal_mean(Dataframe,por=0):
    return Dataframe.fillna(value = np.random.normal(loc=Dataframe.mean(),scale=Dataframe.std()))


def df_fillna_dropna_mix(Dataframe,por=0):
    n = Dataframe.isna().sum(axis=0)
    if por == 0 or por *n < 1:
        n = 1
        por = 1
    aux_Dataframe = Dataframe.fillna(value = np.random.normal(loc=Dataframe.mean(),scale=1+Dataframe.std()),limit= int(por*n))
    return aux_Dataframe.dropna()



def Kolmogorov_condition(threshold,n,m):
    c_t = np.sqrt(-np.log(threshold/2)*0.5)
    return c_t * np.sqrt((n+m)/(n*m))



def Kolmogorov_test(new_df,old_df,column,threshold,na_action=df_dropna,por=0):
    new_data = na_action(new_df[column],por)
    old_data = na_action(old_df[column],por)
    ks_statistic, p_value = kstest(new_data, old_data)
    size_n = len(new_data)
    size_m = len(old_data)
    condition = Kolmogorov_condition(threshold,size_n,size_m)
    if ks_statistic > condition:
        return("No cumple",ks_statistic, p_value)
    return("Cumple",ks_statistic, p_value)




def Mann_Whitney_Test(new_df,old_df,column,threshold,na_action=df_dropna,por=0):
    u_statistic, p_value = mannwhitneyu(na_action(new_df[column],por), na_action(old_df[column],por))
    if p_value < threshold:
        return("No cumple",u_statistic, p_value)
    return("Cumple",u_statistic, p_value)


def Tester(new_df,old_df,column,threshold,na_action=df_dropna,por = 0):
    KS_results = list(Kolmogorov_test(new_df,old_df,column,threshold,na_action,por))
    MW_results = list(Mann_Whitney_Test(new_df,old_df,column,threshold,na_action,por))
    return {"KS":KS_results,"MW":MW_results}


def test_distribuciones(FILENAME,PATH_TEST_DICC,PREV_DICC,TEST_COLUMNS,SIGNIFICANCIA):
    tests = pd.DataFrame(columns=['Test', 'Resultado'])
    new_df =pd.read_csv(PATH_TEST_DICC,delimiter=";")
    old_df = pd.read_csv(PREV_DICC,delimiter=";")
    for i in range(len(TEST_COLUMNS)):
        resultados_aux = Tester(new_df,old_df,TEST_COLUMNS[i],SIGNIFICANCIA,na_action=df_dropna,por = 0)
        tests.loc[len(tests)] = [f'Kolmogorov_Smirnov_{TEST_COLUMNS[i]}', resultados_aux["KS"]]
        tests.loc[len(tests)] = [f'Mann_Whitney_{TEST_COLUMNS[i]}', resultados_aux["MW"]]
    tests.to_csv(FILENAME, index=False)
    return tests
    
