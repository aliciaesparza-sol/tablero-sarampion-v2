import os
import subprocess

repo_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\INFORME AUTOMATIZADO SARAMPION\ESTRATEGIA-SARAMPI-N-2026-main"
workflow_dir = os.path.join(repo_path, ".github", "workflows")
os.makedirs(workflow_dir, exist_ok=True)
workflow_file = os.path.join(workflow_dir, "diario.yml")

workflow_content = """name: Reporte Diario SRMPN

# Este archivo configura GitHub para que corra el reporte solito todos los días
on:
  schedule:
    # Se activa a las 6:45 AM hora de Durango (CST), que son las 12:45 UTC
    - cron: '45 12 * * *'
  workflow_dispatch:  # Este botón te permite correrlo a mano cuando quieras desde la web

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Descargar el código del repositorio
      uses: actions/checkout@v4
    
    - name: Configurar Python (versión 3.12)
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
        cache: 'pip' # Activa el caché automático de librerías de Python

    - name: Instalar librerías del sistema (Optimizado)
      run: |
        sudo NEEDRESTART_MODE=a DEBIAN_FRONTEND=noninteractive apt-get update
        sudo NEEDRESTART_MODE=a DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf2.0-0 shared-mime-info
        
    - name: Cache de Navegador Playwright
      uses: actions/cache@v4
      id: playwright-cache
      with:
        path: ~/.cache/ms-playwright
        key: ${{ runner.os }}-playwright-v1-${{ hashFiles('WBSCRPR/requirements.txt') }}

    - name: Instalar librerías de Python
      run: |
        python3 -m pip install --upgrade pip
        pip3 install -r requirements.txt
        pip3 install -r WBSCRPR/requirements.txt
        
    - name: Preparar el navegador automatizado
      if: steps.playwright-cache.outputs.cache-hit != 'true'
      run: |
        playwright install chromium --with-deps
        
    - name: Instalar dependencias de Playwright (si no hubo cache hit)
      if: steps.playwright-cache.outputs.cache-hit == 'true'
      run: playwright install-deps chromium
        
    - name: "Paso 1: Entrar a CENSIA y bajar los datos nuevos"
      env:
        CENSIA_USER: ${{ secrets.CENSIA_USER }}
        CENSIA_PASS: ${{ secrets.CENSIA_PASS }}
      run: |
        python3 WBSCRPR/spider.py
        
    - name: "Paso 2: Procesar los datos y crear el Reporte PDF"
      run: |
        chmod +x srmpn
        # Buscamos el archivo que se acaba de descargar
        CSV_FILE=$(ls -t datos/*.csv | head -n1)
        echo "Procesando archivo: $CSV_FILE"
        ./srmpn "$CSV_FILE"
        
    - name: "Paso 3: Enviar el correo con los resultados"
      env:
        GMAIL_USER: ${{ secrets.GMAIL_USER }}
        GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
        MAIL_TO: ${{ secrets.MAIL_TO }}
      run: |
        python3 WBSCRPR/dispatcher.py
        
    - name: Guardar copias de seguridad de lo generado (por 90 días)
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: reporte_diario_artefactos
        path: |
          salida/*.pdf
          salida/*.md
          salida/*.png
          datos/*.csv
          *.png
"""

with open(workflow_file, "w", encoding="utf-8") as f:
    f.write(workflow_content)
print("Workflow file created at:", workflow_file)

try:
    print("Running: git add .github/workflows/diario.yml")
    subprocess.check_call(['git', 'add', '.github/workflows/diario.yml'], cwd=repo_path)
    
    print("Running: git commit")
    subprocess.check_call(['git', 'commit', '-m', 'Add GitHub Actions workflow for daily report'], cwd=repo_path)
    
    print("Running: git push origin main")
    # Using check_output to capture credentials prompt or error message if it hangs
    res = subprocess.check_output(['git', 'push', 'origin', 'main'], cwd=repo_path, stderr=subprocess.STDOUT)
    print("Push succeeded:")
    print(res.decode('utf-8'))
except Exception as e:
    print("Git commands failed:", e)
