import numpy as np
import pandas as pd

def alarma_2(resultado_dist,resultado_series,threshold):
    passed = True
    n = pd.shape(resultado_dist)[0] + pd.shape(resultado_series)[0]
    n_passed = 0
    for index, test in resultado_dist.iterrows():
        if test["Resultado"][0] == "Cumple":
            n_passed += 1
        else:
            failed_test = test["Test"]
            print(f"El test {failed_test} fallo \n")
    for index, test in resultado_series.iterrows():
        if test["Resultado"][0] == "Cumple":
            n_passed += 1
        else:
            failed_test = test["Test"]
            print(f"El test {failed_test} fallo \n")
    if n_passed < threshold:
        passed = False
    return passed






    