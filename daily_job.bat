@echo off
setlocal
cd /d "C:\Users\aicil\.gemini\antigravity\scratch"

echo ===================================================
echo  ACTUALIZACION DIARIA - TABLERO SARAMPION
echo  Fecha: %date% %time%
echo ===================================================

echo.
echo [1/4] Descargando CSV actualizado de CeNSIA...
python auto_update_censia.py
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo la descarga de CeNSIA. Abortando.
    exit /b 1
)

echo.
echo [2/4] Procesando datos y generando data.json...
python actualizar_tablero_v2.py
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo el procesamiento de datos. Abortando.
    exit /b 1
)

echo.
echo [3/4] Copiando data.json al tablero React y compilando...
copy /Y "charts\cobertura_municipal_latest.json" "sarampion-dashboard\public\data.json"
cd sarampion-dashboard
call npm run build
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Fallo la compilacion del tablero. Abortando.
    cd ..
    exit /b 1
)
cd ..

echo.
echo [4/4] Publicando en GitHub Pages (rama master)...
robocopy sarampion-dashboard\dist . /E /XD .git node_modules /XF .gitignore
git add -A
git commit -m "Auto Update: %date% - Datos CeNSIA actualizados" || echo Sin cambios nuevos.
git push origin main:master --force

echo.
echo ===================================================
echo  Proceso completado exitosamente a las %time%
echo ===================================================
