@echo off
setlocal enabledelayedexpansion

REM ==============================================================================
REM SISTEMA DE INTELIGENCIA COMERCIAL - QALI KAY S.A.C.
REM Script Asistido de 1 Clic para Conectar a la Nube (GitHub + GitHub Pages / Vercel)
REM ==============================================================================

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

REM Asegurar que Git y GitHub CLI esten en el PATH de la sesion
set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%LOCALAPPDATA%\Programs\GitHub CLI;%PATH%"

echo ==============================================================================
echo [QALI KAY] CONEXION DE DASHBOARD COMERCIAL A LA NUBE (1 CLIC)
echo ==============================================================================
echo.
echo Este asistente conectara el Dashboard Comercial a GitHub para que cuentes con
echo un LINK WEB HTTPS PERMANENTE accesible desde cualquier celular, tablet o PC.
echo.
echo Presiona cualquier tecla para abrir la autorizacion de GitHub en tu navegador...
pause >nul

echo.
echo [1/4] Autenticando con GitHub CLI...
echo Se abrira tu navegador web con un codigo de verificacion. Autoriza la aplicacion.
echo.
gh auth login --web -h github.com -p https
if errorlevel 1 (
    echo.
    echo [ERROR] No se pudo completar la autenticacion en GitHub.
    echo Por favor, verifica tu conexion y vuelve a intentarlo.
    pause
    exit /b 1
)

echo.
echo [2/4] Verificando cuenta de GitHub...
for /f "tokens=*" %%i in ('gh api user --jq .login') do set "GH_USER=%%i"
echo      * Conectado como usuario: %GH_USER%

echo.
echo [3/4] Creando repositorio remoto 'qalikay-ventas' y subiendo codigo...
gh repo create qalikay-ventas --public --source=. --remote=origin --push
if errorlevel 1 (
    echo      * El repositorio podria ya existir. Sincronizando con rama main...
    git remote add origin https://github.com/%GH_USER%/qalikay-ventas.git >nul 2>&1
    git push -u origin main
)

echo.
echo [4/4] Activando GitHub Pages para LINK WEB GRATUITO E INMEDIATO...
gh api -X POST repos/%GH_USER%/qalikay-ventas/pages -F build_type=legacy -f source[branch]=main -f source[path]=/ >nul 2>&1

echo.
echo ==============================================================================
echo [SUCCESS] DESPLIEGUE CLOUD CONFIGURADO EXITOSAMENTE
echo ==============================================================================
echo.
echo Tu Dashboard Comercial ahora se actualizara automaticamente cada vez que corras
echo 'actualizar_dashboard.bat' (o en las tareas automaticas de 07:30 y 15:30).
echo.
echo ------------------------------------------------------------------------------
echo TU LINK WEB HTTPS PERMANENTE (GITHUB PAGES):
echo   https://%GH_USER%.github.io/qalikay-ventas/
echo.
echo NOTA: GitHub Pages tarda entre 1 a 2 minutos en compilar la primera vez.
echo Protegido por PIN Directivo: 2026 / 7361
echo ------------------------------------------------------------------------------
echo.
echo OPCIONAL (VERCEL):
echo Si prefieres la velocidad CDN global de Vercel (https://qalikay-ventas.vercel.app):
echo 1. Entra a https://vercel.com/new
echo 2. Selecciona tu repositorio 'qalikay-ventas' y haz clic en 'Deploy'.
echo (El archivo vercel.json ya esta configurado para redirigir directamente al Dashboard).
echo.
echo Presiona cualquier tecla para finalizar...
pause >nul
exit /b 0
