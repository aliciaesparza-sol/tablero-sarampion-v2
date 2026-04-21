import pandas as pd
import numpy as np
from difflib import get_close_matches

# --- 1. Load Doses from temporary copy ---
doses_path = r"C:\Users\aicil\.gemini\antigravity\scratch\FORMATO_TEMP.xlsx"
df_doses = pd.read_excel(doses_path, sheet_name='ANEXO B', header=None)

vaccination_records = []
for i in range(6, 21): 
    row = df_doses.iloc[i]
    if pd.isna(row[4]): continue
    vaccination_records.append({
        "locality_orig": str(row[4]).strip(),
        "srp": row[24] if not pd.isna(row[24]) else 0,
        "sr": row[25] if not pd.isna(row[25]) else 0,
        "total_doses": row[26] if not pd.isna(row[26]) else 0,
        "source": str(row[29])
    })

# --- 2. Load Population from PFAM with Area of Influence logic ---
pfam_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\MICRO PFAM2025.xlsx"
df_pfam = pd.read_excel(pfam_path, sheet_name='MEZQUITAL', header=None)

# We'll build a map of Locality -> Population
# We'll also track the "Current Area Total"
locality_pop_map = {}
current_area_total = 0
area_localities = []

for i in range(len(df_pfam)-1, 11, -1): # Backwards to propagate totals up?
    # No, forwards is better to identify the "Head" of the area.
    pass

# Let's do forwards and look ahead for the "TOTAL AREA" row?
# Actually, the file structure seems to be: HEAD LOCALITY, then sub-localities, then TOTAL row.
# We'll collect localities in a list and when we hit TOTAL, assign that total to all.

area_groups = []
current_group = []
for i in range(12, len(df_pfam)):
    row = df_pfam.iloc[i]
    name = str(row[1]).strip()
    if 'TOTAL AREA DE INFLUENCIA' in name:
        pop = row[7]
        try:
            pop = float(pop)
        except:
            pop = 0
        for loc in current_group:
            locality_pop_map[loc['name']] = {"pop": pop, "inegi": loc['inegi']}
        current_group = []
    elif name != 'nan' and not 'TOTAL' in name:
        current_group.append({"name": name, "inegi": str(row[0])})

# --- 3. Matching and Calculation ---
results = []
pfam_names = list(locality_pop_map.keys())

for rec in vaccination_records:
    orig = rec["locality_orig"]
    # Clean name for matching
    target = orig.split('(')[0].split(',')[0].strip()
    if "SAN FRANCISCO DE OCOTAN" in orig.upper():
        target = "SAN FRANCISCO DEL MEZQUITAL" # Known major unit
    
    matches = get_close_matches(target, pfam_names, n=1, cutoff=0.5)
    match_info = None
    if matches:
        match_info = locality_pop_map[matches[0]]
        match_name = matches[0]
    else:
        match_name = "No match"
        match_info = {"pop": 0, "inegi": "N/A"}
    
    pop = match_info['pop']
    inegi = match_info['inegi']
    
    reach = (rec["total_doses"] / pop * 100) if pop > 0 else 0
    
    results.append({
        "Localidad": orig,
        "Referencia PFAM": match_name,
        "INEGI": inegi,
        "Población": round(pop, 0),
        "Dosis": rec["total_doses"],
        "Alcance (%)": round(reach, 2)
    })

# --- 4. Export ---
df_results = pd.DataFrame(results)
output_csv = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\Reporte_Alcance_Mezquital_2025.csv"
df_results.to_csv(output_csv, index=False)

print("--- Resumen de Alcance ---")
print(df_results.to_string())
