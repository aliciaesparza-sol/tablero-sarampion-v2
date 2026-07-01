import pandas as pd
import os
import re

# Paths (adjust if needed)
csv_path = r"C:/Users/aicil/OneDrive/Escritorio/PVU/ANEXOS DGO/Anexos_Durango.csv"
excel_path = r"C:/Users/aicil/OneDrive/Escritorio/PVU/ANEXOS DGO/VACUNACIÓN ANEXOS FINAL.xlsx"
output_md = r"C:/Users/aicil/.gemini/antigravity-ide/scratch/vaccination_report.md"

# Load CSV with latin-1 encoding (semicolon-separated)
try:
    df_csv = pd.read_csv(csv_path, delimiter=';', encoding='latin-1')
except Exception as e:
    raise RuntimeError(f"Failed to read CSV: {e}")

# Load Excel (first sheet)
try:
    df_excel = pd.read_excel(excel_path, engine='openpyxl')
except Exception as e:
    raise RuntimeError(f"Failed to read Excel: {e}")

# Identify columns of interest
# CSV columns (based on preview):
# no;edo;num;nom_leg;nom_com;dir;mun;modelo;tel;lat;lon;query_usado;status;maps_url
csv_center_code_col = 'num'
csv_center_name_col = 'nom_com'

# Excel columns we saw:
# 'Marca temporal', 'Nombre (s)', 'Apellido paterno', 'Apellido materno',
# 'Fecha de nacimiento (DD/MM/AA)', 'Sexo', 'Edad cimplida en a�os',
# 'Domicilio', 'Municipio y localidad', 'Celular', 'Tel fijo', 'Admnistraci�n de vacunas'
excel_address_col = 'Domicilio'
excel_vaccines_col = 'Admnistraci�n de vacunas'

# Prepare a mapping from center code to center name for quick lookup
center_map = {}
for _, row in df_csv.iterrows():
    code = str(row[csv_center_code_col]).strip()
    name = str(row[csv_center_name_col]).strip()
    center_map[code] = name

# We'll build a nested dict: {center_name: {vaccine: count}}
summary = {}

# Helper to split vaccine list (commas and possibly spaces)
def split_vaccines(vacc_str):
    if pd.isna(vacc_str):
        return []
    # Replace common delimiters (commas, ';') with commas
    vacc_str = str(vacc_str).replace(';', ',')
    parts = [p.strip() for p in vacc_str.split(',') if p.strip()]
    return parts

# For each Excel row, try to find matching center by checking if any center name appears in the address
for idx, row in df_excel.iterrows():
    address = str(row.get(excel_address_col, ''))
    vaccines = split_vaccines(row.get(excel_vaccines_col, ''))
    if not vaccines:
        continue
    # Find matching center code by searching address for any center name from CSV
    matched_code = None
    matched_name = None
    for code, name in center_map.items():
        # Simplify strings for containment check
        if name.lower() in address.lower():
            matched_code = code
            matched_name = name
            break
    # If no match, fall back to using municipality if present
    if not matched_name:
        municipio = str(row.get('Municipio y localidad', '')).lower()
        for code, name in center_map.items():
            if name.lower() in municipio:
                matched_code = code
                matched_name = name
                break
    # If still no match, skip this record (cannot associate with a center)
    if not matched_name:
        continue
    # Initialize dicts
    if matched_name not in summary:
        summary[matched_name] = {}
    for vac in vaccines:
        summary[matched_name][vac] = summary[matched_name].get(vac, 0) + 1

# Build markdown report
lines = []
lines.append('# Informe Ejecutivo de Vacunación en Centros de Rehabilitación – Durango')
lines.append('')
lines.append('## Tabla de dosis aplicadas por centro y biológico')
lines.append('')
lines.append('| Centro | Biológico | Dosis aplicadas |')
lines.append('|---|---|---|')
for center, vac_dict in summary.items():
    for vac, cnt in vac_dict.items():
        lines.append(f'| {center} | {vac} | {cnt} |')
lines.append('')
# Totales por centro
lines.append('## Totales de dosis por centro')
lines.append('')
lines.append('| Centro | Total dosis aplicadas |')
lines.append('|---|---|')
for center, vac_dict in summary.items():
    total = sum(vac_dict.values())
    lines.append(f'| {center} | {total} |')
lines.append('')
lines.append('### Resumen ejecutivo')
lines.append('')
lines.append('Se presentan los resultados de la vacunación realizada en los centros de rehabilitación del estado de Durango durante el período analizado. La tabla muestra la distribución de dosis administradas por cada centro y por cada biológico (vacuna). Los totales por centro permiten identificar la cobertura y focalizar acciones de refuerzo donde sea necesario.')

# Write markdown file
with open(output_md, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('Reporte generado en', output_md)
