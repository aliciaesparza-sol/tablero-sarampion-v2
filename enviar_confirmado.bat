@echo off
setlocal
cd /d "C:\Users\aicil\.gemini\antigravity-ide\scratch"

echo ============================================================
echo  ENVIANDO INFORME DIARIO A TODOS LOS CONTACTOS (GRUPO)
echo  Fecha: %date%   Hora: %time%
echo ============================================================
echo.

python enviar_correo.py

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] No se pudo enviar el correo a los contactos.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  Envio completado exitosamente.
echo ============================================================
pause
