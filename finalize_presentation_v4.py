import shutil
import os
import re
import json

base_dir = r"C:\Users\aicil\.gemini\antigravity\scratch"
# Usamos Institucional.html (v5.1) como plantilla
html_path = os.path.join(base_dir, "Institucional.html")
semaforo_path = os.path.join(base_dir, "charts", "semaforo.json")
analysis_path = os.path.join(base_dir, "charts", "analysis_v4.json")
output_path = os.path.join(base_dir, "index.html")
images_output_dir = os.path.join(base_dir, "images")

if not os.path.exists(images_output_dir):
    os.makedirs(images_output_dir)

# Read files
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

with open(semaforo_path, 'r', encoding='utf-8') as f:
    semaforo_data = json.load(f)

with open(analysis_path, 'r', encoding='utf-8') as f:
    analysis_data = json.load(f)

# Inject Data
html_content = html_content.replace('SEMAFORO_DATA_PLACEHOLDER', json.dumps(semaforo_data))
html_content = html_content.replace('ANALYSIS_DATA_PLACEHOLDER', json.dumps(analysis_data))

# Handle Images (Extracting from Base64 or Source if needed)
# In this template (Institucional.html), images were already Base64. 
# But for the dynamic charts (like cobertura_por_indicador.png), we'll ensure they are handled.

def process_images_src(match):
    img_src = match.group(1)
    
    # Si ya es base64, lo dejamos como está o intentamos extraerlo?
    # Para reducir el tamaño del HTML, lo ideal es NO tener base64.
    
    if img_src.startswith("data:image"):
        return match.group(0) # Maintain existing for now if it was already there (logos)
    
    # For dynamic chart images from the 'charts' folder
    img_name = os.path.basename(img_src)
    src_img_path = os.path.join(base_dir, "charts", img_name)
    
    if os.path.exists(src_img_path):
        dest_img_path = os.path.join(images_output_dir, img_name)
        shutil.copy2(src_img_path, dest_img_path)
        return f'src="images/{img_name}"'
    
    return match.group(0)

# Replace <img src="..."> references to chart images
new_content = re.sub(r'src="([^"]+\.png)"', process_images_src, html_content)

# Clean up 2025 remnants and set to 2026 / Semana 13
new_content = new_content.replace("2025", "2026")
new_content = new_content.replace("22/03/2026", "29/03/2026")
new_content = new_content.replace("22 de marzo", "29 de marzo")
new_content = new_content.replace("Semana 12", "Semana 13")
new_content = new_content.replace("Semana 53", "Semana 13") # From old template
new_content = new_content.replace("Cierre de 2025", "Avance de 2026")

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Tablero Institucional v5.1 (2026) creado en: {output_path} para la fecha 29/03/2026")
