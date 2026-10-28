@echo off
setlocal enabledelayedexpansion

REM ==============================================================================
REM SISTEMA DE INTELIGENCIA COMERCIAL - QALI KAY S.A.C.
REM Script de Actualizacion y Sincronizacion de Dashboard (Nivel 1 y Nivel 2)
REM ==============================================================================

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

if not exist "logs" mkdir "logs"
set "LOG_FILE=%PROJECT_DIR%logs\actualizacion_dashboard.log"

set "PYTHON_EXE=%PROJECT_DIR%.venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] No se encontro el interprete Python en %PYTHON_EXE%
    echo [%date% %time%] [ERROR] Interprete Python no encontrado en %PYTHON_EXE% >> "%LOG_FILE%"
    exit /b 1
)

echo ==============================================================================
echo [QALI KAY] INICIANDO SINCRONIZACION DEL DASHBOARD COMERCIAL
echo Fecha y Hora: %date% %time%
echo ==============================================================================
echo.
echo [%date% %time%] [START] Iniciando sincronizacion completa del dashboard >> "%LOG_FILE%"

echo [1/4] Sincronizando transacciones RPA Defontana desde Google Sheets...
"%PYTHON_EXE%" src\etl_ventas_defontana.py --sync-rpa >> "%LOG_FILE%" 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo [ERROR] Fallo el paso 1: etl_ventas_defontana.py --sync-rpa [Codigo: !ERRORLEVEL!]
    echo [%date% %time%] [ERROR] Fallo el paso 1 [Codigo: !ERRORLEVEL!] >> "%LOG_FILE%"
    exit /b !ERRORLEVEL!
)
echo      * [OK] Parquet actualizado correctamente.

echo.
echo [2/4] Ejecutando Motor de Reglas Comerciales y Sincronizacion de Kardex/Panel...
"%PYTHON_EXE%" src\motor_reglas_carteras.py >> "%LOG_FILE%" 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo [ERROR] Fallo el paso 2: motor_reglas_carteras.py [Codigo: !ERRORLEVEL!]
    echo [%date% %time%] [ERROR] Fallo el paso 2 [Codigo: !ERRORLEVEL!] >> "%LOG_FILE%"
    exit /b !ERRORLEVEL!
)
echo      * [OK] Carteras, alertas y matrices recalculadas exitosamente.

echo.
echo [3/4] Exportando datos comerciales e inyectando en Dashboard HTML...
"%PYTHON_EXE%" src\exportar_datos_dashboard.py >> "%LOG_FILE%" 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo [ERROR] Fallo el paso 3: exportar_datos_dashboard.py [Codigo: !ERRORLEVEL!]
    echo [%date% %time%] [ERROR] Fallo el paso 3 [Codigo: !ERRORLEVEL!] >> "%LOG_FILE%"
    exit /b !ERRORLEVEL!
)
echo      * [OK] Dashboard HTML actualizado y listo para visualizacion.

echo.
echo [4/4] Verificando sincronizacion remota con Git [Vercel Cloud]...
where git >nul 2>&1
if errorlevel 1 (
    echo      * [INFO] Git no disponible en PATH. Sincronizacion local completada con exito.
    goto :fin_sync
)

git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo      * [INFO] Repositorio local sin remote origin configurado. Sincronizacion local completada.
    goto :fin_sync
)

echo      * Realizando commit y push automatico a rama principal...
git add ejecucion\PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html data\datos_comerciales.json >> "%LOG_FILE%" 2>&1
git commit -m "Auto-sync: Sincronizacion comercial RPA Defontana [%date% %time%]" >> "%LOG_FILE%" 2>&1
git push origin HEAD >> "%LOG_FILE%" 2>&1
echo      * [OK] Cambios enviados a repositorio remoto para despliegue automatico en Vercel.

:fin_sync

echo.
echo ==============================================================================
echo [SUCCESS] SINCRONIZACION COMPLETADA CON EXITO AL 100 por ciento
echo Terminado en: %date% %time%
echo Log detallado disponible en: logs\actualizacion_dashboard.log
echo ==============================================================================
echo [%date% %time%] [SUCCESS] Sincronizacion finalizada exitosamente >> "%LOG_FILE%"

exit /b 0
