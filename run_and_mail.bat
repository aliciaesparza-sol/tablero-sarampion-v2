@echo off
setlocal
cd /d "C:\Users\aicil\.gemini\antigravity-ide\scratch"

echo ===================================================
echo  PROCESO DE INFORME DIARIO - GENERACION Y ENVIO
echo  Fecha: %date% %time%
echo ===================================================

echo.
echo [1/2] Generando informe diario actualizado...
:: Aquí llamamos al script de generación de informe de vacunación. 
:: Puedes cambiar "generar_informe.py" por "generar_informe_conasabi.py" u otro según necesites.
python generar_informe.py
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Falló la generación del informe. Abortando envío de correo.
    exit /b 1
)

echo.
echo [2/2] Enviando informe por correo electronico...
python enviar_correo.py
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Falló el envío del correo electrónico.
    exit /b 1
)

echo.
echo ===================================================
echo  Proceso completado exitosamente a las %time%
echo ===================================================
