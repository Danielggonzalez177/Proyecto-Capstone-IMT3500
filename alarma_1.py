


def alarma_1(resultados_logicos):
    passed = True
    for test in resultados_logicos:
        if test[1] != "Cumple":
            print(f"El test de {test[0]} no paso")
            passed = False
    return passed
