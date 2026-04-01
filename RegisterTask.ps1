$action = New-ScheduledTaskAction -Execute "C:\Users\aicil\.gemini\antigravity\scratch\daily_job.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At 18:00
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Actualizacion_Sarampion_CeNSIA" -Description "Descarga datos de CeNSIA y actualiza tablero en GitHub Pages."
