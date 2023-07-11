# Capstone - Validación de Datos ITAU
## Isolation Forest

Este archivo contiene información sobre las funciones implementadas para la parte de Isolation Forest del proyecto Capstone - Validación de Datos ITAU. El objetivo de esta parte del proyecto es revisar, de manera automatizada, outliers en un subconjunto de las variables de las bases de datos, por medio de modelos de Isolation Forest de **Sklearn** implementados en Python 3.8+. El archivo principal que utiliza el método automatizado es ``Test_Isolation.py``, pero también se presentan funciones extra en ``IsolationForest.ipynb`` con el fin de poder hacer un análisis más allá del método automatizado si así lo desea el banco. La visualización de las bases de datos se realizó con **Matplotlib** y **PCA** de sklearn para la reducción de dimensionalidad. Los links para instalar estas librerías se encuentran a continuación.

## Librerías utilizadas e instalación

- Numpy ([Instalación](https://numpy.org/install/))
- Pandas ([Instalación](https://pandas.pydata.org/docs/getting_started/install.html))
- Matplotlib ([Instalación](https://matplotlib.org/stable/users/installing/index.html))
- Sklearn ([Instalación](https://scikit-learn.org/stable/install.html))
- IPython ([Instalación](https://ipython.org/install.html))
- Shap ([Instalación](https://shap.readthedocs.io/en/latest/index.html)) (opcional para visualizacion)

## Lectura y parámetros
Hay algunos parámetros usados para el correcto funcionamiento de los tests. En cuanto a los parámetros:
- `PATH_XXYY`: Objeto tipo `str` que contiene la ruta a la base de datos que contiene la fecha `XXYY`.
- `MONEDA_CODS`: Objeto tipo `list` que contiene los tipos de moneda válidos, en base al diccionario de datos entregado. 
- `BANCO_CODS`: Objeto tipo `list` que contiene los bancos válidos, en base al diccionario de datos entregado. 
- `DICC_X`: Objeto auxiliar tipo `list` que contiene los campos válidos para la variable `X`, en base al diccionario de datos entregado. 
- `UMBRAL`: #Por implementar#, `dict` que contiene los umbrales a usar por columna.
- ``CONTAMINATION``: Proporción de outliers esperados en la base de datos.
- ``N_ESTIMATORS``: Cantidad de **iTrees** a usar (árboles de decisión de iForest). 

## Funciones

A continuación se muestran las funciones para implementar los tests. Aquí `df` representa un `pandas.DataFrame`.

- `iso_forest2(df, contamination=0.1, n_estimators=100, n_components=2)`: Recibe base de datos `df`, donde `contamination` representa una estimación de los outliers esperados en la base de datos, `n_estimators` es la cantidad de iTrees generados, y `n_components` es una opción de visualización (en 2d o 3d). Es relevante notar también que esta función solo recibe ``df`` con columnas **numéricas**, y además **no puede contener NaNs** en las columnas a evaluar. En caso de querer integrar variables **categóricas** al modelo, en el archivo ``IsolationForest.ipynb`` asociado se explica cómo hacerlo, por medio de **OneHotEncoding**. 
- ``test_isolation(PATH_TEST_DICC,CONTAMINACION,FILENAME_ISOLATION,COLUMNAS_ISOLATIONN_ESTIMATORS)``: recibe ``PATH`` a leer, parámetros de ``CONTAMINACION, N_ESTIMATORS`` como en ``iso_forest2``, escribe los resultados en ``FILENAME_ISOLATION.csv``, y ``COLUMNAS_ISOLATION`` son las columnas a testear.
-  ``shap.Explainer(iForest, df)``: Funcion de la libreria **SHAP**, capaz de explicar las tendencias en modelos. En nuestro caso, se utiliza para ver las columnas que más influyen en la clasificación de outliers.
-  ``find_contamination(df)``: Función para estimar parámetro de contaminación por método de EM y MV, explicados abajo. La función es bastante lenta y en realidad no es necesaria puesto que asumimos contaminacion de 0.1, pero queda implementada en caso de que el banco quiera probar su funcionamiento y encontrar parámetros más óptimos.
- ``em(t, t_max, volume_support, s_unif, s_X, n_generated)``: Funcion utilizada para calcular el metodo de Excess Mass.
- ``mv(axis_alpha, volume_support, s_unif, s_X, n_generated)``: Funcion utilizada para calcular el metodo de Mass Volume.

El fundamento teórico de las dos últimas funciones puede ser encontrado [aqui](https://arxiv.org/abs/1607.01152), y el repositorio de Github de donde se sacaron los códigos asociados ([aqui](https://github.com/ngoix/EMMV_benchmarks/blob/master/em.py)).

