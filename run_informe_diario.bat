@echo off
setlocal
cd /d "C:\Users\aicil\.gemini\antigravity-ide\scratch"

echo ============================================================
echo  INFORME DIARIO AUTOMATIZADO - SARAMPION DURANGO
echo  Fecha: %date%   Hora: %time%
echo ============================================================

python informe_diario_sarampion.py >> "log_informe_diario.txt" 2>&1

IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] El proceso falló. Revisa log_informe_diario.txt
    exit /b 1
)

echo.
echo ============================================================
echo  Proceso completado exitosamente a las %time%
echo ============================================================
