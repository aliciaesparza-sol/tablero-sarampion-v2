import pandas as pd
from pathlib import Path
import numpy as np
import unicodedata

def normalize_name(name):
    if pd.isna(name): return ""
    name = str(name).strip().upper()
    name = "".join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    name = name.replace('Ñ', 'N').replace('DDEL', 'DEL')
    return name

# Paths
output_file = Path(r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA POR MUNICIPIO Y SEMANA EPIDEMIOLÒGICA\Cobertura_Antes_Mayo_2025_Por_Municipio.xlsx")
source_file = Path("temp.xlsx")
pop_path = Path(r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO 3\Poblacion_municipio_edad_simple_y_sexo_Mexico_2026_CENJSIA_EGM.xlsx")
doses_6a_path = Path(r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA POR MUNICIPIO Y SEMANA EPIDEMIOLÒGICA\COBERTURAS POR MUNICIPIO SRP Y SR 2025 12M,18M Y 6A POR SEMANA EPIDEMIOLOGICA.xlsx")

# --- Step 1: Existing Extraction Logic ---
xl = pd.ExcelFile(source_file)
target_sheets = {
    '1 Año': '12 Meses (1ra)',
    '18 Meses': '18 Meses (2da)',
    'Rezag 2-12 Años': '6 Años (2da - Rezag)'
}
available_sheets = xl.sheet_names
all_data = []

for base_sheet, new_name in target_sheets.items():
    exact_sheet = next((s for s in available_sheets if base_sheet.replace('ñ', 'n') in s.replace('ñ', 'n') or base_sheet in s), None)
    if not exact_sheet: continue
    try:
        df = pd.read_excel(source_file, sheet_name=exact_sheet, header=3)
        cols = df.columns
        mun_col = next((c for c in cols if 'municipio' in str(c).lower()), None)
        meta_col = next((c for c in cols if 'meta' in str(c).lower() and 'sect' in str(c).lower()), None)
        cubos_col = next((c for c in cols if 'cubos' in str(c).lower() and 'ene-may' in str(c).lower()), None)
        
        if mun_col and meta_col and cubos_col:
            temp_df = df[[mun_col, meta_col, cubos_col]].copy()
            temp_df.columns = ['Municipio', 'Meta Sectorial', 'Dosis Antes Mayo 2025']
            temp_df = temp_df[temp_df['Municipio'].notna()]
            temp_df = temp_df[~temp_df['Municipio'].astype(str).str.contains('Total|TOTAL|JURISDICCIÓN|jurisdicción', case=False)]
            temp_df['Grupo Etario'] = new_name
            temp_df['Meta Sectorial'] = pd.to_numeric(temp_df['Meta Sectorial'], errors='coerce').fillna(0)
            temp_df['Dosis Antes Mayo 2025'] = pd.to_numeric(temp_df['Dosis Antes Mayo 2025'], errors='coerce').fillna(0)
            temp_df['Cobertura (%)'] = np.where(temp_df['Meta Sectorial'] > 0, (temp_df['Dosis Antes Mayo 2025'] / temp_df['Meta Sectorial']) * 100, 0)
            all_data.append(temp_df)
    except Exception as e:
        print(f"Error processing {exact_sheet}: {e}")

# --- Step 2: Specific 6 Year Coverage Calculation Pestaña ---
try:
    # 2.1 Load Population 6y
    df_pop_raw = pd.read_excel(pop_path, sheet_name='Durango', header=3)
    pop_muni_names = df_pop_raw.iloc[0, 1:40].tolist()
    pop_values = df_pop_raw.iloc[8, 1:40].tolist() # Row 8 is Age 6
    pop_df = pd.DataFrame({'Municipio_Raw': pop_muni_names, 'Poblacion_6y': pop_values})
    pop_df['Muni_Norm'] = pop_df['Municipio_Raw'].apply(normalize_name)
    
    # 2.2 Load Doses 6y
    df_doses_raw = pd.read_excel(doses_6a_path, sheet_name='SE 53', header=5)
    # Col 0: Municipio, Col 8: Dosis 6A
    doses_df = df_doses_raw.iloc[:, [0, 8]].copy()
    doses_df.columns = ['Municipio_Raw', 'Dosis_6y']
    doses_df = doses_df[doses_df['Municipio_Raw'].notna()]
    doses_df = doses_df[~doses_df['Municipio_Raw'].astype(str).str.contains('TOTAL', case=False)]
    doses_df['Muni_Norm'] = doses_df['Municipio_Raw'].apply(normalize_name)
    
    # 2.3 Merge and Calculate
    merged_6y = pd.merge(pop_df, doses_df[['Muni_Norm', 'Dosis_6y']], on='Muni_Norm', how='left')
    merged_6y['Dosis_6y'] = pd.to_numeric(merged_6y['Dosis_6y'], errors='coerce').fillna(0)
    merged_6y['Poblacion_6y'] = pd.to_numeric(merged_6y['Poblacion_6y'], errors='coerce').fillna(0)
    merged_6y['Cobertura_6y (%)'] = np.where(merged_6y['Poblacion_6y'] > 0, (merged_6y['Dosis_6y'] / merged_6y['Poblacion_6y']) * 100, 0)
    
    calc_6y_df = merged_6y[['Municipio_Raw', 'Poblacion_6y', 'Dosis_6y', 'Cobertura_6y (%)']].copy()
    calc_6y_df.columns = ['Municipio', 'Población Meta (6 años)', 'Doses Aplicadas (6 años)', 'Cobertura (%)']
    calc_6y_df['Cobertura (%)'] = calc_6y_df['Cobertura (%)'].map(lambda x: f"{x:.1f}%")
except Exception as e:
    print(f"Error calculating specific 6y coverage: {e}")
    calc_6y_df = None

# --- Step 3: Write to Excel ---
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    numeric_df = final_df.copy()
    
    consolidado = numeric_df.pivot_table(index='Municipio', columns='Grupo Etario', values=['Meta Sectorial', 'Dosis Antes Mayo 2025', 'Cobertura (%)'], aggfunc='mean', fill_value=0)
    # Reorder columns
    grupos = [target_sheets['1 Año'], target_sheets['18 Meses'], target_sheets['Rezag 2-12 Años']]
    flattened_cols = []
    for g in grupos:
        if g in consolidado['Meta Sectorial'].columns:
            flattened_cols.append(('Meta Sectorial', g))
            flattened_cols.append(('Dosis Antes Mayo 2025', g))
            flattened_cols.append(('Cobertura (%)', g))
    consolidado = consolidado[flattened_cols]
    consolidado.columns = [f"{val} {grp}" for val, grp in consolidado.columns]
    consolidado.reset_index(inplace=True)
    for col in consolidado.columns:
        if 'Cobertura' in col: consolidado[col] = consolidado[col].map(lambda x: f"{x:.1f}%")

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        if calc_6y_df is not None:
            calc_6y_df.to_excel(writer, sheet_name='Cálculo 2da Dosis 6 Años', index=False)
        consolidado.to_excel(writer, sheet_name='Consolidado General', index=False)
        final_df[['Municipio', 'Grupo Etario', 'Meta Sectorial', 'Dosis Antes Mayo 2025', 'Cobertura (%)']].to_excel(writer, sheet_name='Detalle', index=False)
        
    print(f"Successfully updated Excel file: {output_file}")
