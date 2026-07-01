import pandas as pd
import os

file_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\POBLACIÓN\POBLACION 2026\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx'
df = pd.read_excel(file_path, sheet_name='Durango')

# Find column index for Mezquital
mezquital_col_idx = None
for idx, val in enumerate(df.iloc[3]):
    if str(val).strip() == 'Mezquital':
        mezquital_col_idx = idx
        break

if mezquital_col_idx is None:
    print("Could not find Mezquital column!")
    exit(1)

# Extract Hombres and Mujeres datasets
hombres_df = df.iloc[5:115].copy()
hombres_df['Edad'] = df.iloc[5:115, 0].astype(int)
hombres_df['Hombres'] = df.iloc[5:115, mezquital_col_idx].astype(int)

mujeres_df = df.iloc[123:233].copy()
mujeres_df['Edad'] = df.iloc[123:233, 0].astype(int)
mujeres_df['Mujeres'] = df.iloc[123:233, mezquital_col_idx].astype(int)

# Merge on Edad
merged = pd.merge(hombres_df[['Edad', 'Hombres']], mujeres_df[['Edad', 'Mujeres']], on='Edad')
merged['Total'] = merged['Hombres'] + merged['Mujeres']

# Full age-by-age dict
pop_h = {row['Edad']: row['Hombres'] for _, row in merged.iterrows()}
pop_m = {row['Edad']: row['Mujeres'] for _, row in merged.iterrows()}
pop_t = {row['Edad']: row['Total'] for _, row in merged.iterrows()}

tot_hombres = df.iloc[5:115, mezquital_col_idx].astype(int).sum()
tot_mujeres = df.iloc[123:233, mezquital_col_idx].astype(int).sum()
grand_total = tot_hombres + tot_mujeres

# Under 49 (0 to 49 years old)
sum_h_0_49 = merged[merged['Edad'] <= 49]['Hombres'].sum()
sum_m_0_49 = merged[merged['Edad'] <= 49]['Mujeres'].sum()
sum_t_0_49 = merged[merged['Edad'] <= 49]['Total'].sum()

# Helper function to compute groups
def get_group_data(ages, meta_factor):
    universo = sum(pop_t[a] for a in ages)
    universo_h = sum(pop_h[a] for a in ages)
    universo_m = sum(pop_m[a] for a in ages)
    
    meta_h = round(universo_h * meta_factor)
    meta_m = round(universo_m * meta_factor)
    meta_t = round(universo * meta_factor)
    
    return {
        'univ_h': universo_h, 'univ_m': universo_m, 'univ_t': universo,
        'meta_h': meta_h, 'meta_m': meta_m, 'meta_t': meta_t
    }

# Compute all groups
groups = {
    '6-11 meses': get_group_data([0], 0.5), # 50% of age 0
    '1 año': get_group_data([1], 1.0), # 100% of age 1
    '18 meses': get_group_data([1], 1.0), # 100% of age 1 (proxied as age 1)
    '6 años': get_group_data([6], 1.0), # 100% of age 6
    '2 a 12 años': get_group_data(range(2, 13), 0.5), # 50% of ages 2-12
    '13 a 19 años': get_group_data(range(13, 20), 0.5), # 50% of ages 13-19
    '20 a 39 años': get_group_data(range(20, 40), 0.5), # 50% of ages 20-39
    '40 a 49 años': get_group_data(range(40, 50), 0.5), # 50% of ages 40-49
}

# Generate Markdown report
md_content = f"""# Población del Municipio de Mezquital, Durango (Proyección 2026)

Este reporte contiene los datos de población para el municipio de **Mezquital, Durango** correspondientes a la proyección de 2026, incluyendo la población total, población de 0 a 49 años y el desglose por grupos etarios solicitados.

---

## 1. Resumen General

| Categoría | Hombres | Mujeres | Total |
| :--- | :---: | :---: | :---: |
| **Población Total** (Todas las edades) | {tot_hombres:,} | {tot_mujeres:,} | **{grand_total:,}** |
| **Población de 0 a 49 años** | {sum_h_0_49:,} | {sum_m_0_49:,} | **{sum_t_0_49:,}** |

---

## 2. Cuadro Resumen por Grupos Etarios (CENJSIA)

> [!NOTE]
> La **Población Meta** se calcula aplicando los porcentajes de cobertura objetivo definidos por los lineamientos del CENJSIA sobre la **Población Universo** (población real en la proyección).
> Los grupos etarios pueden presentar solapamientos (ej. *18 meses* y *1 año* se calculan sobre la población de 1 año; *6 años* es un subconjunto de *2 a 12 años*).

| Grupo Etario | Factor de Cálculo | Universo Hombres | Universo Mujeres | Universo Total | Meta Hombres | Meta Mujeres | Meta Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **6-11 meses** | 50% de 0 años | {groups['6-11 meses']['univ_h']:,} | {groups['6-11 meses']['univ_m']:,} | {groups['6-11 meses']['univ_t']:,} | {groups['6-11 meses']['meta_h']:,} | {groups['6-11 meses']['meta_m']:,} | **{groups['6-11 meses']['meta_t']:,}** |
| **1 año** | 100% de 1 año | {groups['1 año']['univ_h']:,} | {groups['1 año']['univ_m']:,} | {groups['1 año']['univ_t']:,} | {groups['1 año']['meta_h']:,} | {groups['1 año']['meta_m']:,} | **{groups['1 año']['meta_t']:,}** |
| **18 meses** | 100% de 1 año | {groups['18 meses']['univ_h']:,} | {groups['18 meses']['univ_m']:,} | {groups['18 meses']['univ_t']:,} | {groups['18 meses']['meta_h']:,} | {groups['18 meses']['meta_m']:,} | **{groups['18 meses']['meta_t']:,}** |
| **6 años** | 100% de 6 años | {groups['6 años']['univ_h']:,} | {groups['6 años']['univ_m']:,} | {groups['6 años']['univ_t']:,} | {groups['6 años']['meta_h']:,} | {groups['6 años']['meta_m']:,} | **{groups['6 años']['meta_t']:,}** |
| **2 a 12 años** | 50% del grupo | {groups['2 a 12 años']['univ_h']:,} | {groups['2 a 12 años']['univ_m']:,} | {groups['2 a 12 años']['univ_t']:,} | {groups['2 a 12 años']['meta_h']:,} | {groups['2 a 12 años']['meta_m']:,} | **{groups['2 a 12 años']['meta_t']:,}** |
| **13 a 19 años** | 50% del grupo | {groups['13 a 19 años']['univ_h']:,} | {groups['13 a 19 años']['univ_m']:,} | {groups['13 a 19 años']['univ_t']:,} | {groups['13 a 19 años']['meta_h']:,} | {groups['13 a 19 años']['meta_m']:,} | **{groups['13 a 19 años']['meta_t']:,}** |
| **20 a 39 años** | 50% del grupo | {groups['20 a 39 años']['univ_h']:,} | {groups['20 a 39 años']['univ_m']:,} | {groups['20 a 39 años']['univ_t']:,} | {groups['20 a 39 años']['meta_h']:,} | {groups['20 a 39 años']['meta_m']:,} | **{groups['20 a 39 años']['meta_t']:,}** |
| **40 a 49 años** | 50% del grupo | {groups['40 a 49 años']['univ_h']:,} | {groups['40 a 49 años']['univ_m']:,} | {groups['40 a 49 años']['univ_t']:,} | {groups['40 a 49 años']['meta_h']:,} | {groups['40 a 49 años']['meta_m']:,} | **{groups['40 a 49 años']['meta_t']:,}** |

---

## 3. Desglose Detallado por Edad Simple (0 a 49 años)

A continuación se detalla la población por cada año de edad, dividida en Hombres y Mujeres:

| Edad | Hombres | Mujeres | Total |
| :---: | :---: | :---: | :---: |
"""

for _, row in merged.iterrows():
    md_content += f"| {row['Edad']} | {row['Hombres']:,} | {row['Mujeres']:,} | {row['Total']:,} |\n"

# Save to the artifacts directory
artifact_dir = r"C:\Users\aicil\.gemini\antigravity-ide\brain\e759dd4d-50d6-4002-b290-f895f5101ec8"
artifact_path = os.path.join(artifact_dir, "mezquital_population_under_49.md")

with open(artifact_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"Report successfully updated at {artifact_path}")
