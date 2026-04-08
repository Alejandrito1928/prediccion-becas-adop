import pandas as pd
import numpy as np
import math
import re
import warnings
warnings.filterwarnings('ignore')

def clean_deporte(val):
    val = str(val).upper().strip()
    val = val.replace('Á','A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U').replace('Ü','U')
    if 'CARRETERA' in val: return 'CARRETERA'
    if 'PISTA' in val: return 'PISTA'
    if 'NATACION' in val: return 'NATACION'
    if 'ATLETISMO' in val: return 'ATLETISMO'
    if 'TRIATLON' in val: return 'TRIATLON'
    if 'PIRAGUISMO' in val: return 'PIRAGUISMO'
    return val

def clean_puesto_final(val):
    val_str = str(val).upper().strip()
    if pd.isna(val) or val_str in ['NAN', 'NO PARTICIPO', 'SIN DATOS', 'NO PARTICIPÓ']:
        return -1
    val_str_clean = re.sub(r'[A-Z]\d+', '', val_str)
    nums = re.findall(r'\d+', val_str_clean)
    if not nums:
        return -1
    nums_int = [int(n) for n in nums]
    resultado = math.ceil(sum(nums_int) / len(nums_int))
    return -1 if resultado > 11 else resultado

def clean_cat(val):
    if pd.isna(val): return 'NO'
    v = str(val).upper().replace('Á','A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U')
    if 'MANTENEMOS PROMESA' in v or 'NO ADOP' in v:
        return 'NO'
    for cat in ['ORO', 'PLATA', 'BRONCE', 'ELITE', 'PRO']:
        if cat in v:
            return cat
    return 'NO' 

def calcular_tendencia(row):
    diccionario_niveles = {'NO': 0, 'PRO': 1, 'ELITE': 2, 'BRONCE': 3, 'PLATA': 4, 'ORO': 5}
    if row['TIENE_HISTORICO'] == 0:
        return 0
    else:
        nivel_num = diccionario_niveles.get(row['NIVEL'], 0)
        return row['CONTRASTE'] - nivel_num

def limpiar_datos(df):
    df_limpio = df.copy()
    
    # 1. Selección de columnas
    col_id = df_limpio.filter(like='ID').columns[0]
    col_dep = df_limpio.filter(like='DEPORTE').columns[0]
    col_puesto = df_limpio.filter(like='CTO REF').columns[0] 
    col_cont = df_limpio.filter(like='CONTRASTE').columns[0]
    col_niv = df_limpio.filter(like='NIVEL').columns[0]
    col_pan = df_limpio.filter(like='PANEL').columns[0]
    col_motivo = df_limpio.filter(like='MOTIVO PANEL').columns[0] 
    col_prop = df_limpio.filter(like='PROPUESTA').columns[0]
    
    df_limpio = df_limpio[[col_id, col_dep, col_puesto, col_cont, col_niv, col_pan, col_motivo, col_prop]].copy()
    df_limpio.columns = ['ID', 'DEPORTE', 'PUESTO', 'CONTRASTE', 'NIVEL', 'PANEL', 'MOTIVO', 'PROPUESTA']
    
    # 2. Borrar filas indeseadas
    df_limpio = df_limpio[~df_limpio['PANEL'].astype(str).str.upper().str.contains('NO', na=False)]
    df_limpio = df_limpio[~df_limpio['NIVEL'].astype(str).str.upper().str.contains('ESPECIAL', na=False)]
    df_limpio = df_limpio[~df_limpio['PROPUESTA'].astype(str).str.upper().str.contains('EMBARAZO', na=False)]
    
    # 3. Limpieza de celdas
    df_limpio['DEPORTE'] = df_limpio['DEPORTE'].apply(clean_deporte)
    df_limpio['PUESTO'] = df_limpio['PUESTO'].apply(clean_puesto_final)
    df_limpio['CONTRASTE'] = df_limpio['CONTRASTE'].apply(clean_puesto_final)
    df_limpio['NIVEL'] = df_limpio['NIVEL'].apply(clean_cat)
    df_limpio['PROPUESTA'] = df_limpio['PROPUESTA'].apply(clean_cat)
    
    # 4. Variables calculadas
    df_limpio['PARTICIPACION'] = df_limpio['PUESTO'].apply(lambda x: 0 if x == -1 else 1)
    df_limpio['TIENE_HISTORICO'] = df_limpio['NIVEL'].apply(lambda x: 0 if x == 'NO' else 1)
    df_limpio['TENDENCIA'] = df_limpio.apply(calcular_tendencia, axis=1)
    
    return df_limpio