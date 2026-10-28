@echo off
setlocal enabledelayedexpansion

REM ==============================================================================
REM SISTEMA DE INTELIGENCIA COMERCIAL - QALI KAY S.A.C.
REM Asistente de 1 Clic para Conectar a la Nube (GitHub + GitHub Pages / Vercel)
REM ==============================================================================

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

set "PYTHON_EXE=%PROJECT_DIR%.venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] No se encontro el interprete Python en %PYTHON_EXE%
    pause
    exit /b 1
)

"%PYTHON_EXE%" src\conectar_nube.py

echo Presiona cualquier tecla para cerrar esta ventana...
pause >nul
exit /b 0
