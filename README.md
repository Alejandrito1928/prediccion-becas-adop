<div align="center">

# 🏆 Proyecto Capstone: Optimización Algorítmica de Becas ADOP

**Sistema F.A.I.R. de Inteligencia Artificial para la predicción objetiva y auditable de becas deportivas del Comité Paralímpico Español (CPE).**

*Proyecto desarrollado dentro del programa Samsung Innovation Campus por el equipo **"Atletas del Dato"**.*

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)

</div>

---

## 🚀 Visión General
El **Plan ADOP** asigna recursos a los deportistas de élite hacia los Juegos Paralímpicos. Este proyecto elimina la "caja negra" algorítmica y los sesgos cognitivos mediante la implementación de un **Oráculo Híbrido** de Machine Learning que asiste a la dirección técnica del comité.

## 🧠 Arquitectura del Modelo
Debido a la severa restricción muestral (Micro-Dataset), se descartó el Deep Learning en favor de una arquitectura robusta de Machine Learning clásico:

* **Random Forest "Acorazado":** Algoritmo ajustado con `class_weight='balanced'` y `max_depth=4` para evitar el sesgo conservador y proteger la sensibilidad hacia la clase minoritaria (Beca ORO).
* **Consenso Matemático:** El modelo fusiona una estimación probabilística categórica (Clasificador) con una penalización estricta de distancias ordinales.
* **100% Explicabilidad (SHAP):** Uso de gráficos *Waterfall* para traducir la decisión matemática a lenguaje humano, justificando el mérito exacto de cada variable.

## 🔒 Cumplimiento Legal y RGPD (Protocolo Zero Trust)
Este repositorio opera bajo un estricto acuerdo de confidencialidad (NDA).
* **Datos Anonimizados:** No se incluyen nombres, DNI ni datos reales de los atletas.
* **Data Distillery:** El sistema utiliza identificadores de fila e imputaciones matemáticas que protegen la identidad y el historial médico, asegurando el cumplimiento total del RGPD.

## 📂 Estructura del Proyecto
* `/src`: Scripts de la fase de Producción (ETL y Pipeline).
* `/models`: Archivos `.pkl` serializados (Cerebro de la IA).
* `/interface`: Aplicación interactiva diseñada en Streamlit (Próximamente).
* `/docs`: Documentación y reportes de validación cruzada.

---
<div align="center">
  <b>Desarrollado por el equipo "Atletas del Dato":</b><br><br>
  <a href="URL_DE_TU_LINKEDIN">Héctor Alejandro. Novoa</a> | 
  <a href="URL_DEL_LINKEDIN_DE_OSCAR">Oscar F. González</a> | 
  <a href="URL_DEL_LINKEDIN_DE_CARLOS">Carlos Vaquero</a>
</div>