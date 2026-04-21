import pandas as pd
import numpy as np
from difflib import get_close_matches

# --- 1. Load Doses from temporary copy ---
doses_path = r"C:\Users\aicil\.gemini\antigravity\scratch\FORMATO_TEMP.xlsx"
df_doses = pd.read_excel(doses_path, sheet_name='ANEXO B', header=None)

vacc_records = []
for i in range(6, 21): 
    row = df_doses.iloc[i]
    if pd.isna(row[4]) or str(row[4]).strip() == "": continue
    vacc_records.append({
        "loc": str(row[4]).strip(),
        "total": row[26] if not pd.isna(row[26]) else 0
    })

# --- 2. Load Population from PFAM ---
pfam_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\MICRO PFAM2025.xlsx"
df_pfam = pd.read_excel(pfam_path, sheet_name='MEZQUITAL', header=None)

locality_data = {}
temp_group = []

for i in range(12, len(df_pfam)):
    row = df_pfam.iloc[i]
    name = str(row[1]).strip()
    inegi = str(row[0]).strip() if not pd.isna(row[0]) else "N/A"
    
    if "TOTAL AREA DE INFLUENCIA" in name:
        pop_val = row[8] # INDEX 8!
        try:
            pop_val = float(pop_val)
            if np.isnan(pop_val): pop_val = 0
        except:
            pop_val = 0
        
        for loc_name, loc_inegi in temp_group:
            locality_data[loc_name] = {"pop": pop_val, "inegi": loc_inegi}
        temp_group = []
    elif name != 'nan' and "TOTAL" not in name:
        temp_group.append((name, inegi))

# Handle leftovers if file doesn't end with TOTAL row
if temp_group:
    for loc_name, loc_inegi in temp_group:
        locality_data[loc_name] = {"pop": 0, "inegi": loc_inegi}

# --- 3. Join and Calculate ---
results = []
pfam_names = list(locality_data.keys())

for item in vacc_records:
    orig_name = item['loc']
    # Cleaning target for better matching
    target = orig_name.split('(')[0].split(',')[0].replace("Mezquital", "").strip()
    if "SAN FRANCISCO DE OCOTAN" in orig_name.upper():
        target = "SAN FRANCISCO DEL MEZQUITAL"
    
    matches = get_close_matches(target, pfam_names, n=1, cutoff=0.3)
    if matches:
        match_name = matches[0]
        pop = locality_data[match_name]['pop']
        inegi = locality_data[match_name]['inegi']
    else:
        match_name = "Not found"
        pop = 0
        inegi = "N/A"
    
    reach = (item['total'] / pop * 100) if pop > 0 else 0
    
    results.append({
        "Localidad": orig_name,
        "Ref PFAM": match_name,
        "INEGI": inegi,
        "Población": int(pop),
        "Dosis": int(item['total']),
        "Alcance (%)": round(reach, 2)
    })

df_reach = pd.DataFrame(results)
output_csv = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\Reporte_Alcance_Mezquital_2025.csv"
df_reach.to_csv(output_csv, index=False)

print(df_reach.to_markdown(index=False))
