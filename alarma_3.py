import numpy as np
import pandas as pd

def alarma_3(resultado,threshold):
    passed = True
    test_comparison = resultado[-2]
    jump = resultado[-1]
    resultado = resultado[:-2]
    resultado = resultado[::-1]
    j = 1
    for i in range(len(resultado)):
        if resultado[i] >= test_comparison and i < len(resultado)-1 and j == 1:
            change = (resultado[i+1] - resultado[i])/(jump)
            j = 0
            if change > threshold:
                passed = False
                print("Isolation Forest encuentra demasiadas filas como outliers o cerca de serlo \n")
                return passed
    return passed

            


    
    
        