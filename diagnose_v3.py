import pandas as pd
import unicodedata
import json
import shutil
import os

xl_pop = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO SARAMPION\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx'
csv_nom = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO SARAMPION\SRP-SR-2025_21-03-2026 08-11-38.csv'
xl_ref = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA POR MUNICIPIO Y SEMANA EPIDEMIOLÒGICA\COBERTURA_SARAMPION_POR_MUNICIPIO_CORTE18MARZO2026.xlsx'

tmp_ref = r'C:\Users\aicil\.gemini\antigravity\scratch\temp_ref.xlsx'
shutil.copy2(xl_ref, tmp_ref)

def norm(s):
    if pd.isna(s): return ""
    return unicodedata.normalize('NFD', str(s).upper()).encode('ascii', 'ignore').decode('utf-8').strip()

# 1. Compare names
pop = pd.read_excel(xl_pop, sheet_name='Durango', header=None)
nom = pd.read_csv(csv_nom, encoding='latin1')

pop_names = [str(x) for x in pop.iloc[4, 1:].dropna().unique() if x != 'Durango']
nom_names = [str(x) for x in nom['MUNICIPIO'].dropna().unique()]

p_norm = {norm(n): n for n in pop_names}
n_norm = {norm(n): n for n in nom_names}

unmatched_nom = [n for n in nom_names if norm(n) not in p_norm]
unmatched_pop = [p for p in pop_names if norm(p) not in n_norm]

# 2. Extract Excel Ref Layout (Sheet 1 Año)
ref_xl = pd.ExcelFile(tmp_ref)
df_ref = pd.read_excel(tmp_ref, sheet_name='1 Año', header=None)

# Look for header row
header_row = -1
for i in range(len(df_ref)):
    if 'Municipio' in df_ref.iloc[i].values:
        header_row = i
        break

ref_cols = df_ref.iloc[header_row].tolist() if header_row != -1 else []

results = {
    'unmatched_nom': unmatched_nom,
    'unmatched_pop': unmatched_pop,
    'ref_sheets': ref_xl.sheet_names,
    'ref_1year_cols': [str(c) for c in ref_cols]
}

with open(r'C:\Users\aicil\.gemini\antigravity\scratch\diag_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Diagnostic complete.")
