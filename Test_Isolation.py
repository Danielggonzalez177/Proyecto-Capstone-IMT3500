import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA



def get_nan_cols(df, nan_percent=0.8):
    'Retorna columnas con porcentaje NaN mayor a nan_percent'
    threshold = len(df.index) * nan_percent
    return [c for c in df.columns if sum(df[c].isnull()) >= threshold]  



def iso_forest2(df, contamination, n_estimators=100, n_components=2):
    'Primero hacemos iForest, luego PCA'

    if 'is_anomaly_prediction' in df.columns:
        df.drop(columns=['is_anomaly_prediction'], axis=1, inplace=True)
    if 'iForest_scores' in df.columns:
        df.drop(columns=['iForest_scores', 'iForest_outliers'], axis=1, inplace=True)

    # iForest
    # Hay que hacer cross validation de CONTAMINATION
    iForest = IsolationForest(n_estimators=n_estimators, verbose=0, contamination=contamination)
    iForest.fit(df.values)
    predictions = iForest.predict(df.values)

    # Extract scores
    df["iForest_scores"] = -1*iForest.score_samples(df.values)
    # Extract predictions
    df["iForest_outliers"] = predictions
    # Describe the dataframe
    print('Summary')
    print(df[['iForest_scores', 'iForest_outliers']].describe())

    # Standardize features
    df_scaled = StandardScaler().fit_transform(df)
    # Define dimensions = 2
    pca = PCA(n_components=n_components)
    # Conduct the PCA
    principal_comp = pca.fit_transform(df_scaled)
    # Convert to dataframe

    pca_df = pd.DataFrame(data = principal_comp, columns = [f'PC{i+1}' for i in range(n_components)])

    print('Prediciones:', df.iForest_outliers.value_counts())

    if n_components == 2:
        fig, ax = plt.subplots(1,1, figsize=(10,8))
        plt.scatter(pca_df.PC1, pca_df.PC2, c=df.iForest_scores, cmap='RdBu')
        plt.title(f'iForest scores, $\lambda = {contamination}$')
        plt.colorbar(label='iForest outliers')
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        plt.show()
    elif n_components == 3:
        fig = plt.figure(figsize=(10,8))
        ax = fig.add_subplot(projection='3d')
        ax.scatter(pca_df.PC1, pca_df.PC2, pca_df.PC3, c=df.iForest_scores, cmap='RdBu')
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_zlabel('PC3')
    else:
        print('No es posible visualizar resultados para mas componentes')

    return df.iForest_scores, df.iForest_outliers




def test_isolation(PATH_DICC_TEST,CONTAMINACION,FILENAME,LISTA_COLUMNA):
    df = pd.read_csv(PATH_DICC_TEST,delimiter=";")
    df = df[LISTA_COLUMNA].dropna()
    df_scores,df_outliers = iso_forest2(df,CONTAMINACION)
    testing = np.linspace(0,1,100)
    result = [0] * 100
    n = len(df_scores)
    test_comparison = df_outliers[df_outliers == -1].count()/len(df_outliers)
    for i in range(len(testing)):
        result[i] = df_scores[df_scores >= testing[i]].count()/n
    result.append(test_comparison)
    result.append(1/100)
    tests = pd.DataFrame(columns=['Test', 'Resultado'])
    tests.loc[len(tests)] = ["Outliers segun Isolation",test_comparison]
    for i in range(len(testing)):
        tests.loc[len(tests)] = [f"Outliers con probabilidad de {testing[i]}",result[i]]
    tests.to_csv(FILENAME, index=False)
    return result
    