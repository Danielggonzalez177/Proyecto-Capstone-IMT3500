# Capstone - Validación de Datos ITAU
## Tests Series
#Se encuentra en el archivo Tests_Series.py
Este archivo contiene información sobre las funciones implementadas para la parte de series de tiempo para 
determinar la presencia de autocorrelación tanto positiva como negativa o inconcluso del proyecto Capstone - Validación de Datos ITAU. 
El objetivo de esta parte del proyecto es revisar, si los datos entre tiempo presentan autocorrelación tanto como positiva, negativa o no se pueden obtener conclusiones Python 3.8+.
Para ello el código utiliza las librerías **Numpy**,**Pandas** e importa las funciones norm,durbin_watson de las librerias statsmodels.stats.stattools,scipy.stats respectivamente.
Los links para instalar estas librerías se encuentran a continuación.

## Librerías utilizadas e instalación

- Numpy ([Instalación](https://numpy.org/install/))
- Pandas ([Instalación](https://pandas.pydata.org/docs/getting_started/install.html))
- Statsmodels.stats.stattools ([Instalación](https://www.statsmodels.org/stable/install.html))
- Scipy.stats respectivamente ([Instalación](https://scipy.org/install/))

## Funciones

A continuación se muestran las funciones para implementar los tests. Aquí `df` representa un `pandas.DataFrame`.

- `RutComunes(lista)`: Se le entrega una lista con los PATHS de los diccionarios. Esta función se encarga de retornar una lista con todos los ruts que se encuentren en todos los diccionarios de la lista de PATHS.

- `Data(df)`: Fórmula que utiliza calcular_tamano_muestra, en ella se genera dataframes aleatorios de cierto tamaño de df. Finalmente genera una lista de listas, donde en lista[i][j] accedemos a la posición i,j de la lista. En cada 
 		   lista j se calcula el estadístico de Durbin-Watson para cada una de las fechas del dataframe df.
 		   
 - `calcular_tamano_muestra(N, alpha, p, d)`:  Función que calcula el tamaño de la muestra, en donde N es el tamaño de la data, alpha es el nivel de confianza (0.05 por defecto)
 								    , p es la tasa de error esperado (0.5 por defecto) y d es la precisión de error tolerable (0.05 por defecto).
 								    
- `RutComunes(lista)`:  Se le entrega una lista con los PATHS de los diccionarios. Esta función se encarga de retornar una lista con todos los ruts que se encuentren en todos los diccionarios de la lista de PATHS.


- `TestSeriesDW (df,fecha_1,fecha_2)`:  Fórmula que calcula el estadístico de Durbin-Watson para un dataframe df entre las fechas fecha 1,fecha 2.

- `Test(Variable,lista,valor_maximo,valor_minimo,umbral)`: Test que dado una Variable en el diccionario de variables,la lista de PATHS,y los valores máximos y mínimos del estadístico de Durbin-Watson
											retorna el resultado de cumplimiento en porcentaje del test de Durbin-Watson, en conjunto con los porcentajes. Para ello primero filtra los Ruts con la función
											RutComunes, luego genera un dataframe donde se encuentran todos los valores de la variable en todos
											los tiempos de la lista de los PATHS, a este dataframe lo llama dftemporal. En consecuencia ocupa la función Data aplicada a dftemporal que a su vez usa calcu-
											lar_tamano_muestra para obtener la lista de listas. Finalmente calcula el porcentaje de estadísticos de
											Durbin-Watson que estan dentro de cierto rango de umbrales utilizando el siguiente algoritmo:
											if (menores >= umbral or may >= umbral) or (med >= umbral and  media >= umbral):
        											return ["Cumple",mayores,menores,media,may,men,med]
    											return ["No cumple",mayores,menores,media,may,men,med]
    											
    											En donde:
    											menores:Corresponde a la proporción de valores que son menores o iguales a valor_minimo
    											mayores:Corresponde a la proporción de valores que son mayores o iguales a valor_maximo
    											medias:Corresponde a la proporción de valores que estan entre valor minimo y valor_maximo
    											Es decir los valores menores,mayores,medias corresponden a la proporcion en el Test de Durbin-Watson de
    											que existe evidencia para autocorrelación positiva, no existe evidencia de autocorrelación positiva o el test es inconcluso.
    											Poor otra parte tenemos:
    											may:Corresponde a la proporción de valores que son mayores o iguales a valor_maximo
    											mens:Corresponde a la proporción de valores que son menores o iguales a valor_minimo
    											med:Corresponde a la proporción de valores que son menores o iguales a valor minimo
    											Es decir los valores men,may,med corresponden a la proporcion en el Test de Durbin-Watson de
    											que existe evidencia para autocorrelación negativa, no existe evidencia de autocorrelación negativa o el test es inconcluso.
    											*Notar que may,men,med son calculados con respecto a la formula de Durbin-Watson para la autocorrelación negativa, es decir 4-DW.
    											
    											
    											
`test_series(FILENAME_SERIES,PATH_TEST_DICC,PREV_DICCS,CODIGOS_SERIES)`:Se encarga de la ejecución de Test para todas las variables en CODIGOS_SERIES, en donde PREV_DICCS es la lista de los
													  PATHS de las bases temporales a tratar,PATH_TEST_DICC es la base que no se encuentra en PREV_DICCS y FILENAME_SERIES
													  es un cvs donde se guardan los resultados.La función es utilizada en el archivo main.py. 									
    											
    											
    											
    											
    											
    											
    											
    											
    											
    											
    											