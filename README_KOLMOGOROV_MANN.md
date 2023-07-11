# Capstone - Validación de Datos ITAU
## README de Kolmogorov y Mann-Whitney
Este archivo contiene información sobre las funciones implementadas para la parte de distribuciones del proyecto Capstone - Validación de Datos ITAU. Aqui se especifican las funciones en `Test_Distribuciones.py` y que hacen en cada caso.
## Requerimientos 
- Numpy ([Instalación](https://numpy.org/install/))
- Pandas ([Instalación](https://pandas.pydata.org/docs/getting_started/install.html))
- Scipy ([Instalación](https://scipy.org/install/))
    
## Funciones
- `Kolmogorov_test(new_df,old_df,column,threshold,na_action=df_dropna,por=0)`

Este test esta implementado con scipy a traves de kstest. Esta funcion recibe dos listas de datos y devuelve el estadistico de Kolmogorov y el valor p.
El valor p se tomara como la referencia para decidir si las dos muestras distribuyen igual o no. 
Si p es menor a 0.05 se asume que ambas listas de datos son de distribuciones distintas y si es mayor o igual consideramos que son iguales
Dentro del contexto de las bases de datos se espera que las distribuciones deberian ser iguales por lo que definimos que es correcto si se dice que son iguales e incorrecto si es que el test dice que son diferentes

- `Mann_Whitney_Test(new_df,old_df,column,threshold,na_action=df_dropna,por=0)`

Este test esta implementado con scipy a traves de mannwhitneyu. Esta funcion recibe dos listas de datos y devuelve el estadistico de Mann-Whitney y el valor p.

-  `df_dropna/df_fillna_mean/df_fillna_normal_mean/df_fillna_dropna_mix(Dataframe,por=0)`

Todas estas funciones son para poder recibir metodos de los dataframes como funciones. Su objetivo es manipular los nans. El mas importante y el que se ocupa en realidad es `df_dropna`, el cual simplemente los elimina. Los demas son metodos que sirven para reemplazar por la media, reemplazar con una distribucion normal o con una combinacion. 

- `Kolmogorov_condition(threshold,n,m)`
Esta funcion es para calcular la condicion de rechazo de la hipotesis nula para el Test de Kolmogorov-Smirnov si es que hay muchos datos (como es el caso en todas las columnas). Se toma como entrada el valor de significancia y los tamaños de las muestras

- `Tester(new_df,old_df,column,threshold,na_action=df_dropna,por = 0)`
Esta funcion solo junta las funciones `Kolmogorov_test` y `Mann_Whitney_Test` en un test para devolver ambos resultados juntos.

- `test_distribuciones(FILENAME,PATH_TEST_DICC,PREV_DICC,TEST_COLUMNS,SIGNIFICANCIA)`

Esta funcion es la que es llamada por `main.py`. Sirve como el punto donde se llaman todos los tests y se almacenan los resultados para despues escribirlos en un csv y despues devolverlos.