@echo off
title Sistema ADOP F.A.I.R.
color 0B
echo ===================================================
echo     INICIANDO ORACULO HIBRIDO - SISTEMA F.A.I.R.
echo ===================================================
echo.

:: 1. Forzar a Windows a pararse en esta misma carpeta
cd /d "%~dp0"

echo 1. Activando tu entorno de Python (curso_ia)...
:: Asegurate de que esta ruta a Anaconda es exactamente la tuya
call C:\todo\Anaconda\Scripts\activate.bat curso_ia

echo.
echo 2. Levantando la Web...
:: Como el .bat ya esta al lado de app.py, solo ponemos el nombre directo
streamlit run app.py

pause