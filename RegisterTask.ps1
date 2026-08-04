$action = New-ScheduledTaskAction -Execute "C:\Users\aicil\.gemini\antigravity-ide\scratch\daily_job.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At 18:00
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -TaskName "Actualizacion_Sarampion_CeNSIA" -Description "Descarga datos de CeNSIA y actualiza tablero en GitHub Pages." -Force
