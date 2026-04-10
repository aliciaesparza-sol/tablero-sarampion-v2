@echo off
:: =====================================================
:: ACTUALIZADOR TABLERO SARAMPIÓN — DURANGO
:: Ejecuta el script Python y sube a GitHub
:: =====================================================

cd /d "%~dp0"
echo [%date% %time%] Iniciando actualizacion del tablero...

python actualizar_y_publicar.py >> log_actualizaciones.txt 2>&1

echo [%date% %time%] Proceso terminado. Revisa log_actualizaciones.txt
