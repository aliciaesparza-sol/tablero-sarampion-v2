# Configuración de la tarea programada en Windows para enviar el informe diario por correo
$action = New-ScheduledTaskAction -Execute "C:\Users\aicil\.gemini\antigravity-ide\scratch\run_informe_diario.bat"

# Se ejecuta diariamente a las 07:00 AM.
$trigger = New-ScheduledTaskTrigger -Daily -At 07:00

# Crear configuración que permite ejecutar en batería
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

# Registra la tarea en el programador de Windows (forzando actualización si ya existe)
Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -TaskName "Envio_Informe_Diario_Vacunacion" -Description "Genera el informe diario y lo envia automáticamente por correo electrónico." -Force

Write-Host "✅ Tarea programada 'Envio_Informe_Diario_Vacunacion' registrada exitosamente con soporte de batería."
Write-Host "Se ejecutará todos los días a las 07:00 AM."
