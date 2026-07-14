@echo off
setlocal
cd /d "C:\Users\aicil\.gemini\antigravity-ide\scratch"
rem Generar informe del día (sin modo prueba)
call .\run_informe_diario.bat
if %ERRORLEVEL% neq 0 (
    echo Error al generar el informe
    exit /b %ERRORLEVEL%
)
rem Enviar informe a todo el grupo
call .\enviar_confirmado.bat
