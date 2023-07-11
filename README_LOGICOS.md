# Capstone - Validación de Datos ITAU
## Tests Lógicos

Este archivo contiene información sobre las funciones implementadas para la parte lógica del proyecto Capstone - Validación de Datos ITAU. El objetivo de esta parte del proyecto es revisar, de manera automatizada, los aspectos más generales de las bases de datos, que incluyen unicidad, consistencia, formato, etc, por medio de tests lógicos implementados en Python 3.8+, en su mayoría por medio de la librerías **Pandas** y **Numpy**. La visualización de las bases de datos se realizó con **Matplotlib**. Los links para instalar estas librerías se encuentran a continuación.

## Librerías utilizadas e instalación

- Numpy ([Instalación](https://numpy.org/install/))
- Pandas ([Instalación](https://pandas.pydata.org/docs/getting_started/install.html))
- Matplotlib ([Instalación](https://matplotlib.org/stable/users/installing/index.html))
- IPython ([Instalación](https://ipython.org/install.html))

## Lectura y parámetros
Hay algunos parámetros usados para el correcto funcionamiento de los tests. En cuanto a los parámetros:
- `PATH_XXYY`: Objeto tipo `str` que contiene la ruta a la base de datos que contiene la fecha `XXYY`.
- `MONEDA_CODS`: Objeto tipo `list` que contiene los tipos de moneda válidos, en base al diccionario de datos entregado. 
- `BANCO_CODS`: Objeto tipo `list` que contiene los bancos válidos, en base al diccionario de datos entregado. 
- `DICC_X`: Objeto auxiliar tipo `list` que contiene los campos válidos para la variable `X`, en base al diccionario de datos entregado. 
- `UMBRAL`: Objeto `dict` que contiene los umbrales a usar.

## Funciones

A continuación se muestran las funciones para implementar los tests. Aquí `df` representa un `pandas.DataFrame`.

- `formato(df)`: Retorna `list` de alarmas si columnas de `df` estan en mal formato, de la forma: (formato actual, formato en diccionario), por cada columna que tenga mal formato.
- `duplicidad_id_mov(df)`: Revisa si el indice unico `(RUT, NUMOPE)` es unico, y retorna tupla `(cumplimiento, % error)`.
- `duplicidad_num_cuenta(df)`: Revisa si hay filas duplicadas, y retorna tupla `(cumplimiento, % error)`.
- `fechas_validas(df)`: Revisa si los dias en `FECOPE` estan en formato correcto, y retorna tupla `(cumplimiento, % error)`.
- `fec_movimiento(df)`: Revisa los `NaN` en las fechas, y retorna tupla `(cumplimiento, % error)`.
- `exactitud_intereses(df)`: Revisa la proporcion de `NaN` en `TASAINT`, y retorna tupla `(cumplimiento, % error)`.
- `test_mtorev(df)`: Revisa si `MTOREV` toma valores `0`, y retorna tupla `(cumplimiento, % error)`
- `test_estado(df)`:  Revisa que el estado este entre los valores definidos, y retorna tupla `(cumplimiento, % error)`. Depende de `ESTADO_CODS`.
- `cod_banco(df)`: Revisa que el codigo de banco este entre los valores definidos, y retorna tupla `(cumplimiento, % error)`. Depende de `BANCO_CODS`.
- `cod_divisa(df)`: Verificar que las monedas esten dentro de las definidas, y retorna tupla `(cumplimiento, % error)`. Depende de `MONEDA_CODS`.
- `cod_producto(df)`: Verifica que `CODPRO` este dentro de los valores definidos.
- `cod_tlp(df)`: Verifica que `CODTLP` este dentro de los valores definidos.
- `DIASMORA0_ESTADO1(df)`: Revisa que si `DIASMORA = 0`, entonces `ESTADO = 1`, de acuerdo con el diccionario de datos
- `DIASMORA30_ESTADO2(df)`: Revisa que si `0 < DIASMORA < 30`, entonces `ESTADO = 2`, de acuerdo con el diccionario de datos.
- `DIASMORA89_ESTADO5(df)`: Revisa que si `30 <= DIASMORA <= 89`, entonces `ESTADO = 5`, de acuerdo con el diccionario de datos.
- `test_and_write(df, FILENAME)`: Ejecuta todos los tests anteriores para `df` y crea `FILENAME.csv` que contiene los resultados obtenidos.

