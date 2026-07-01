REM Batch file to run the automated measles report script
@echo off
setlocal
rem Change to the directory containing the script
cd /d "C:\Users\aicil\.gemini\antigravity-ide\scratch"
rem Ensure Python is available (use the system python)
python "informe_diario_sarampion.py" %*
endlocal
