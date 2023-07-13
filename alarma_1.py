import re

def alarma_1(resultados_logicos):
    passed = True
    for index, test in resultados_logicos.iterrows():
        if test["Test"] == "Formato":
            
            lista = test["Resultado"]
            for i in range(len(lista)):
                pattern = r"\((.*?)\)"
                match = re.search(pattern, lista[i].split(":")[0])
                print(f"La columna {match.group(1)} no cumple con el formato especificado \n")
                passed = False

        else:
            if test["Resultado"][0] == 'No cumple':
                print(f"El test de {test['Test']} no cumple\n")
                passed = False
    return passed
