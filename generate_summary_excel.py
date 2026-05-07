import pandas as pd
import json

# 1. LOAD DATA (Re-calculating to be safe)
# --- Locality Data ---
excel_path = r"C:\Users\aicil\.gemini\antigravity\scratch\Formato_Concentrado_Mezquital_2026_Updated.xlsx"
df_exc = pd.read_excel(excel_path, sheet_name="Concentrado", header=None)

manual_pop = {
    "LAS JOYAS": 462, "STA MA. DE OCOTAN": 795, "STA. MA. DE OCOTAN": 795,
    "BAJÍO Y CENTRO": 255, "CARBONERAS": 226, "SAN MANUEL": 41
}

loc_data = {}
for i in range(4, len(df_exc)):
    loc = str(df_exc.iloc[i, 4]).strip().upper()
    if loc == "NAN" or loc == "": continue
    d = pd.to_numeric(df_exc.iloc[i, 61], errors='coerce'); d = d if not pd.isna(d) else 0
    p = pd.to_numeric(df_exc.iloc[i, 82], errors='coerce'); p = p if not pd.isna(p) else 0
    if loc in manual_pop: p = manual_pop[loc]
    if loc not in loc_data: loc_data[loc] = {"Doses": 0, "Population": p}
    loc_data[loc]["Doses"] += d
    if loc_data[loc]["Population"] == 0 and p > 0: loc_data[loc]["Population"] = p

clocs = sorted([{"Localidad": k, "Doses": v["Doses"], "Population": v["Population"]} for k, v in loc_data.items()], key=lambda x: x['Doses'], reverse=True)
df_locs = pd.DataFrame(clocs)
df_locs['Alcance (%)'] = (df_locs['Doses'] / df_locs['Population'] * 100).fillna(0).round(2)

# --- Age Group Data ---
csv_path = r"C:\Descargas_SRP\SRP-SR-2025_04-05-2026 07-59-20.csv"
df_csv = pd.read_csv(csv_path); mez_csv = df_csv[df_csv['MUNICIPIO'] == 'MEZQUITAL']

mapping = {
    "Menores de 1 año (6-11 m)": ["SRP 6 A 11 MESES PRIMERA", "SR 6 A 11 MESES PRIMERA"],
    "1 año": ["SRP 1 ANIO  PRIMERA", "SR 1 ANIO PRIMERA"],
    "2-5 años": ["SRP 2 A 5 ANIOS PRIMERA", "SRP 18 MESES SEGUNDA", "SRP 2 A 5 ANIOS SEGUNDA", "SR 2 A 5 ANIOS PRIMERA", "SR 18 MESES SEGUNDA", "SR 2 A 5 ANIOS SEGUNDA"],
    "6 años": ["SRP 6 ANIOS PRIMERA", "SRP 6 ANIOS SEGUNDA", "SR 6 ANIOS PRIMERA", "SR 6 ANIOS SEGUNDA"],
    "7-9 años": ["SRP 7 A 9 ANIOS PRIMERA", "SRP 7 A 9 ANIOS SEGUNDA", "SR 7 A 9 ANIOS PRIMERA", "SR 7 A 9 ANIOS SEGUNDA"],
    "10-19 años": ["SRP 10 A 12 ANIOS PRIMERA", "SRP 13 A 19 ANIOS PRIMERA", "SRP 10 A 19 ANIOS PRIMERA", "SRP 10 A 12 ANIOS SEGUNDA", "SRP 13 A 19 ANIOS SEGUNDA", "SRP 10 A 19 ANIOS SEGUNDA", "SR 10 A 12 ANIOS PRIMERA", "SR 13 A 19 ANIOS PRIMERA", "SR 10 A 19 ANIOS PRIMERA", "SR 10 A 12 ANIOS SEGUNDA", "SR 13 A 19 ANIOS SEGUNDA", "SR 10 A 19 ANIOS SEGUNDA"],
    "20-29 años": ["SRP 20 A 29 ANIOS PRIMERA", "SRP 20 A 29 ANIOS SEGUNDA", "SR 20 A 29 ANIOS PRIMERA", "SR 20 A 29 ANIOS SEGUNDA"],
    "30-39 años": ["SRP 30 A 39 ANIOS PRIMERA", "SRP 30 A 39 ANIOS SEGUNDA", "SR 30 A 39 ANIOS PRIMERA", "SR 30 A 39 ANIOS SEGUNDA"],
    "40-49 años": ["SRP 40 A 49 ANIOS PRIMERA", "SRP 40 A 49 ANIOS SEGUNDA", "SR 40 A 49 ANIOS PRIMERA", "SR 40 A 49 ANIOS SEGUNDA"],
    "Grupos Especiales": ["SRP PERSONAL DE SALUD PRIMERA", "SRP PERSONAL EDUCATIVO PRIMERA", "SRP JORNALEROS AGRICOLAS PRIMERA", "SRP  PERSONAL DE SALUD SEGUNDA", "SRP  PERSONAL EDUCATIVO SEGUNDA", "SRP JORNALEROS AGRICOLAS SEGUNDA", "SR PERSONAL DE SALUD PRIMERA", "SR PERSONAL EDUCATIVO PRIMERA", "SR JORNALEROS AGRICOLAS PRIMERA", "SR PERSONAL DE SALUD SEGUNDA", "SR PERSONAL EDUCATIVO SEGUNDA", "SR JORNALEROS AGRICOLAS SEGUNDA"]
}

age_list = []
for l, cols in mapping.items():
    d25 = 0; d26 = 0
    for c in cols:
        if c in mez_csv.columns:
            d25 += int(mez_csv[mez_csv['Temporada'] == 2025][c].sum())
            d26 += int(mez_csv[mez_csv['Temporada'] == 2026][c].sum())
    age_list.append({"Grupo de Edad": l, "Doses 2025": d25, "Doses 2026": d26, "Total": d25 + d26})

df_age = pd.DataFrame(age_list)
# Add Population (Manually as done before)
with open("mezquital_pop_conapo.json", "r") as f: pop_c = json.load(f)
pop_m = {"Menores de 1 año (6-11 m)": 1334, "1 año": pop_c["1 year"], "2-5 años": pop_c["2-5 years"], "6 años": pop_c["6 years"], "7-9 años": pop_c["7-9 years"], "10-19 años": pop_c["10-19 years"], "20-29 años": pop_c["20-29 years"], "30-39 años": pop_c["30-39 years"], "40-49 años": pop_c["40-49 years"], "Grupos Especiales": 0}

df_age['Población (CONAPO)'] = df_age['Grupo de Edad'].map(pop_m)
df_age['Cobertura (%)'] = (df_age['Total'] / df_age['Población (CONAPO)'] * 100).fillna(0).round(2)

# Global Total
abs_total_pop = 53894
actual_total = 20977
df_age.loc[len(df_age)] = ["TOTAL MEZQUITAL", df_age['Doses 2025'].sum(), df_age['Doses 2026'].sum(), actual_total, abs_total_pop, round(actual_total/abs_total_pop*100, 2)]

# 2. SAVE TO EXCEL
output_excel = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\INFORMES\Resumen_Vacunacion_Mezquital_2026.xlsx"

with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
    df_locs.to_excel(writer, sheet_name='Dosis por Localidad', index=False)
    df_age.to_excel(writer, sheet_name='Cobertura por Edad', index=False)
    
    # Formatting
    workbook = writer.book
    header_format = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
    total_format = workbook.add_format({'bold': True, 'bg_color': '#F2F2F2', 'border': 1})
    
    for sheet in ['Dosis por Localidad', 'Cobertura por Edad']:
        worksheet = writer.sheets[sheet]
        for col_num, value in enumerate(df_locs.columns if sheet=='Dosis por Localidad' else df_age.columns):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 20)
            
    # Bold the last row in Cobertura
    worksheet = writer.sheets['Cobertura por Edad']
    for col_num, value in enumerate(df_age.iloc[-1]):
        worksheet.write(len(df_age), col_num, value, total_format)

print(f"Excel saved: {output_excel}")
