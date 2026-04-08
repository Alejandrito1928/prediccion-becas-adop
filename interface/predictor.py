import joblib
import pandas as pd
import shap
import matplotlib.pyplot as plt

def predecir_becas(df_limpio):  
    modelo = joblib.load('../models/modelo_rf.pkl')
    
    diccionario_niveles = {'NO': 0, 'PRO': 1, 'ELITE': 2, 'BRONCE': 3, 'PLATA': 4, 'ORO': 5}
    df_ml = df_limpio.copy()
    df_ml['NIVEL'] = df_ml['NIVEL'].map(diccionario_niveles).fillna(0).astype(int)
    
    columnas_modelo = ['PUESTO', 'NIVEL', 'CONTRASTE', 'PARTICIPACION', 'TIENE_HISTORICO', 'TENDENCIA']
    X_nuevo = df_ml[columnas_modelo]
    
    predicciones_numericas = modelo.predict(X_nuevo)
    
    diccionario_inverso = {0: 'NO', 1: 'PRO', 2: 'ELITE', 3: 'BRONCE', 4: 'PLATA', 5: 'ORO'}
    predicciones_texto = [diccionario_inverso.get(p, 'NO') for p in predicciones_numericas]
    
    return predicciones_texto

def explicar_atleta(df_limpio, clase_predicha_texto):
    """Genera el gráfico SHAP para justificar la decisión"""
    modelo = joblib.load('../models/modelo_rf.pkl')
    
    diccionario_niveles = {'NO': 0, 'PRO': 1, 'ELITE': 2, 'BRONCE': 3, 'PLATA': 4, 'ORO': 5}
    df_ml = df_limpio.copy()
    df_ml['NIVEL'] = df_ml['NIVEL'].map(diccionario_niveles).fillna(0).astype(int)
    columnas_modelo = ['PUESTO', 'NIVEL', 'CONTRASTE', 'PARTICIPACION', 'TIENE_HISTORICO', 'TENDENCIA']
    X_nuevo = df_ml[columnas_modelo]
    
    clase_num = diccionario_niveles.get(clase_predicha_texto, 0)
    
    explainer = shap.TreeExplainer(modelo)
    explicacion = explainer(X_nuevo)
    explicacion_clase_ganadora = explicacion[0, :, clase_num]
    
    plt.figure(figsize=(8, 4))
    shap.plots.waterfall(explicacion_clase_ganadora, show=False)
    fig = plt.gcf() 
    plt.close()
    
    return fig