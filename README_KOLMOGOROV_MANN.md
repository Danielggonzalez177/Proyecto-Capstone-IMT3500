# README de Kolmogorov y Mann-Whitney

## Requerimientos 
    -   Scipy
    -   Pandas
    -   Numpy
    

## Kolmogorov

Este test esta implementado con scipy a traves de kstest. Esta funcion recibe dos listas de datos y devuelve el estadistico de Kolmogorov y el valor p.
El valor p se tomara como la referencia para decidir si las dos muestras distribuyen igual o no. 
Si p es menor a 0.05 se asume que ambas listas de datos son de distribuciones distintas y si es mayor o igual consideramos que son iguales
Dentro del contexto de las bases de datos se espera que las distribuciones deberian ser iguales por lo que definimos que es correcto si se dice que son iguales e incorrecto si es que el test dice que son diferentes

## Mann-Whitney

Este test esta implementado con scipy a traves de mannwhitneyu. Esta funcion recibe dos listas de datos y devuelve el estadistico de Mann-Whitney y el valor p.