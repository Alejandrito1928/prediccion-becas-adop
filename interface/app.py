import streamlit as st
import pandas as pd
import time
import io 
import os

import Procesamiento_Web
import Predictor_Web as predictor_Web

st.set_page_config(page_title="Predictor ADOP 2025", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 10rem;}
    </style>
    """, unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_samsung = os.path.join(BASE_DIR, "Imagenes", "samsung.png")
ruta_cpe = os.path.join(BASE_DIR, "Imagenes", "cpe.png")
ruta_upm = os.path.join(BASE_DIR, "Imagenes", "upm.png")

cabecera = st.container()
with cabecera:
    c1, c2, c3 = st.columns([1,1,1])
    # Ahora usamos las rutas calculadas dinámicamente
    with c1: st.image(ruta_samsung, width=150) 
    with c2: st.image(ruta_cpe, width=120)
    with c3: st.image(ruta_upm, width=170)

st.markdown("---")
st.markdown("<h1 style='text-align: center;'>Predictor de Becas ADOP 2025-2028</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Sistema de Ejecución Local (NDA Activo)</p>", unsafe_allow_html=True)
st.write("")
st.write("") 

tab_masiva, tab_individual = st.tabs(["📊 Evaluación Masiva (Archivo Excel)", "👤 Simulador Individual (Registro Manual)"])

with tab_masiva:
    st.write("### 📂 Carga de Datos")
    
    if 'df_final' not in st.session_state:
        st.session_state['df_final'] = None

    archivo_subido = st.file_uploader("Arrastra y suelta aquí el Excel crudo  en formato .xlsx", type=["xlsx"])

    if archivo_subido is not None:
        try:
            df_crudo = pd.read_excel(archivo_subido, sheet_name='Hoja1')
        except Exception:
            df_crudo = pd.read_excel(archivo_subido)
            
        st.success(f"✅ Archivo detectado exitosamente con {len(df_crudo)} deportistas.")
        st.write("---")
        
        if st.button("🚀 Generar Propuestas de Becas", type="primary", use_container_width=True):
            with st.spinner("Prediciendo..."):
                time.sleep(1.5) 
                try:
                    df_limpio = Procesamiento_Web.limpiar_datos(df_crudo)    
                    predicciones_texto = predictor_Web.predecir_becas(df_limpio)
                    
                    df_calculado = df_limpio.copy()
                    df_calculado['Beca Sugerida (IA)'] = predicciones_texto
                    
                    st.session_state['df_final'] = df_calculado
                    
                except Exception as e:
                    st.error(f"❌ Ocurrió un error en la IA. Revisa que el Excel tenga las columnas correctas.")
                    st.error(f"Detalle técnico: {e}")

        if st.session_state['df_final'] is not None:
            df_final = st.session_state['df_final']
            
            st.subheader("📋 Asignación Final Sugerida")
            
            busqueda = st.text_input("🔍 Buscar deportista por ID o Deporte:")
            
            if busqueda:
                df_mostrar = df_final[df_final['ID'].astype(str).str.contains(busqueda, case=False, na=False) | 
                                      df_final['DEPORTE'].astype(str).str.contains(busqueda, case=False, na=False)].copy()
            else:
                df_mostrar = df_final.copy()
                
            df_mostrar['EDAD'] = "Pendiente Fichas"
            df_mostrar['RANKING'] = "Pendiente Fichas"
            
            cols_mostrar = ['ID', 'DEPORTE', 'PUESTO', 'EDAD', 'RANKING', 'Beca Sugerida (IA)']
            st.dataframe(df_mostrar[cols_mostrar], use_container_width=True, hide_index=True)
            st.caption("Nota: Las columnas EDAD y RANKING se activarán visualmente cuando se integren las nuevas fichas de análisis propuestas por el CPE.")

            st.write("---")
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_final.to_excel(writer, index=False, sheet_name='Predicciones')
            
            st.download_button(
                label="📥 Descargar Resultados Oficiales (.xlsx)",
                data=buffer.getvalue(),
                file_name="Predicciones_ADOP.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="secondary",
                use_container_width=True
            )

    else:
        st.info(" Por favor, suba el archivo 'SOLICITUDES ADOP.xlsx' para iniciar la evaluación.")


with tab_individual:
    st.write("### ⚙️ Análisis Manual de Atleta")
    st.write("Ingrese los parámetros deportivos para evaluar a un único atleta mediante IA.")
    
    with st.form("simulador_form"):
        nombre_atleta = st.text_input("Nombre o ID del Deportista", placeholder="Ej. Teresa Perales o AT-01")
        st.markdown("<br>", unsafe_allow_html=True) 

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            input_puesto = st.number_input("Puesto Histórico (CTO REF)", min_value=-1, max_value=100, value=1, help="-1 significa Sin Datos")
            input_participacion = st.selectbox("¿Participó?", options=[1, 0], format_func=lambda x: "Sí (1)" if x==1 else "No (0)")
            
        with col2:
            input_nivel = st.selectbox("Nivel Histórico", options=['ORO', 'PLATA', 'BRONCE', 'ELITE', 'PRO', 'NO'])
            input_historico = st.selectbox("¿Tiene Histórico?", options=[1, 0], format_func=lambda x: "Sí (1)" if x==1 else "No (0)")
            
        with col3:
            input_contraste = st.number_input("Contraste", min_value=-1, max_value=100, value=1)
            input_tendencia = st.number_input("Tendencia Calculada", min_value=-10, max_value=10, value=0)
            
        with col4:
            input_edad = st.number_input("Edad ", min_value=15, max_value=70, value=25, help="Sugerido por CPE")
            input_ranking = st.number_input("Ranking", min_value=1, max_value=100, value=1, help="Sugerido por CPE")
            
        boton_evaluar = st.form_submit_button("🎯 Evaluar Atleta", use_container_width=True)

    if boton_evaluar:
        if nombre_atleta.strip() == "":
            st.warning("⚠️ Por favor, ingresa el Nombre o ID del deportista antes de evaluar.")
        else:
            with st.spinner("Analizando métricas del atleta..."):
                time.sleep(1)
                
                datos_manuales = pd.DataFrame({
                    'NOMBRE': [nombre_atleta],
                    'PUESTO': [input_puesto],
                    'NIVEL': [input_nivel],
                    'CONTRASTE': [input_contraste],
                    'PARTICIPACION': [input_participacion],
                    'TIENE_HISTORICO': [input_historico],
                    'TENDENCIA': [input_tendencia]
                })
                
                prediccion_individual = predictor_Web.predecir_becas(datos_manuales)
                resultado_beca = prediccion_individual[0]
                
                st.write("---")
                
                st.success(f"### 🏅 Beca Sugerida para {nombre_atleta}: **{resultado_beca}**")
                
                st.write(f"### 📊 Justificación Matemática para la beca: {resultado_beca}")
                
                with st.spinner("Generando gráfico de explicabilidad de Oscar..."):
                    figura_shap = predictor_Web.explicar_atleta(datos_manuales, resultado_beca)
                    
                    graf_izq, graf_centro, graf_der = st.columns([1, 2, 1])
                    with graf_centro:
                        st.pyplot(figura_shap)
                        
                    st.info(f"""
                    **Guía de lectura para el Técnico Deportivo (Evaluando la opción {resultado_beca}):**
                    * 🔵 **Méritos:** Datos que impulsan al atleta a ganar esta beca. *(Nota técnica: La interfaz gráfica actual renderiza los méritos en el rojo nativo de SHAP. La paleta Verde/Rojo solicitada se incluirá en la v2.0).*
                    * 🔴 **Riesgos:** Datos que le restan opciones frente a la IA. *(Actualmente renderizado en azul).*
                    * *El tamaño de la barra indica qué parámetro tuvo más peso en la decisión final.*
                    """)
            
    st.markdown("<br><br>", unsafe_allow_html=True)