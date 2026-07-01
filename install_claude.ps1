# Definitive Elevated Installation Script for Claude Desktop
Write-Host "Iniciando reparación e instalación definitiva de Claude..." -ForegroundColor Cyan

# 1. Detener procesos conflictivos
Write-Host "Cerrando WhatsApp y otros procesos en segundo plano..." -ForegroundColor Yellow
Stop-Process -Name *WhatsApp* -Force -ErrorAction SilentlyContinue
Stop-Process -Name *chrome-native-host* -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# 2. Reparar y limpiar la carpeta C:\Program Files\WindowsApps\Deleted
Write-Host "Reparando permisos en la carpeta WindowsApps\Deleted..." -ForegroundColor Yellow
$deletedPath = "C:\Program Files\WindowsApps\Deleted"
if (Test-Path $deletedPath) {
    # Obtener subcarpetas conflictivas
    $subDirs = Get-ChildItem -Path $deletedPath -Directory -ErrorAction SilentlyContinue
    foreach ($dir in $subDirs) {
        $path = $dir.FullName
        if ($path -like "*WhatsApp*") {
            Write-Host "Tomando propiedad de: $path" -ForegroundColor Cyan
            # Ejecutar takeown de forma silenciosa
            cmd.exe /c "takeown /f `"$path`" /r /d y >nul 2>&1"
            # Otorgar control total a Administradores
            cmd.exe /c "icacls `"$path`" /grant administrators:F /t >nul 2>&1"
            # Eliminar la carpeta de forma definitiva
            Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}

# 3. Forzar eliminación del caché corrupto del paquete de Claude
Write-Host "Limpiando el directorio de datos corruptos de Claude..." -ForegroundColor Yellow
$packageFolder = "$env:LOCALAPPDATA\Packages\Claude_pzs8sxrjxfjjc"
if (Test-Path $packageFolder) {
    Remove-Item -Path $packageFolder -Recurse -Force -ErrorAction SilentlyContinue
}

# 4. Registrar el paquete MSIX
Write-Host "Instalando y registrando Claude Desktop..." -ForegroundColor Green
$msixPath = "C:\Users\aicil\AppData\Local\Temp\Claude-1995906102.msix"

try {
    Add-AppxPackage -Path $msixPath -ForceApplicationShutdown -ErrorAction Stop
    Write-Host "¡Claude se ha instalado y registrado correctamente!" -ForegroundColor Green
    Start-Sleep -Seconds 3
} catch {
    Write-Host "Error al registrar el paquete: $_" -ForegroundColor Red
    Write-Host "Intentando instalación directa alternativa..." -ForegroundColor Yellow
    Start-Process -FilePath "C:\Users\aicil\OneDrive\Escritorio\Claude Setup.exe"
}
