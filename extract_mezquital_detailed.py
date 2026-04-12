import pandas as pd
import os

files = {
    'csv': r'c:\Descargas_SRP\SRP-SR-2025_10-04-2026 09-26-01.csv',
    'poblacion': r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO SARAMPION V2\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx',
    'cubo': r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\cubo_sis_consolidado-1.xlsx'
}

# 1. Poblacion - Extract Mezquital 2026 for ages 0-49
print("--- EXTRACTING POBLACION MEZQUITAL ---")
try:
    df_pob = pd.read_excel(files['poblacion'], sheet_name='Durango', header=None)
    # Municipality names are in row 1 (0-indexed)
    mun_row = df_pob.iloc[1]
    mez_col_idx = mun_row[mun_row.astype(str).str.contains('Mezquital', case=False, na=False)].index[0]
    print(f"Mezquital is in column {mez_col_idx}")
    
    # Ages are in column 0, starting from row 3 (0: row 4)
    # We need Hombres and Mujeres.
    # Let's find where 'Hombres' and 'Mujeres' rows start.
    h_idx = df_pob[df_pob[0] == 'Hombres'].index[0]
    m_idx = df_pob[df_pob[0] == 'Mujeres'].index[0]
    print(f"Hombres start at {h_idx}, Mujeres start at {m_idx}")
    
    pop_data = {}
    for age in range(50):
        h_val = df_pob.iloc[h_idx + 1 + age, mez_col_idx]
        m_val = df_pob.iloc[m_idx + 1 + age, mez_col_idx]
        pop_data[age] = float(h_val) + float(m_val)
    print("Population ages 0-5 sample:", {a: pop_data[a] for a in range(6)})
except Exception as e:
    print(f"Error extracting Poblacion: {e}")

# 2. Cubo - Jan-May 2025 doses for Mezquital
print("\n--- EXTRACTING CUBO DOSES ---")
try:
    df_cubo = pd.read_excel(files['cubo'], sheet_name='Cubo SIS Consolidado', header=None)
    # Row 1 has headers like 'Entidad', 'Jurisdicción', 'Municipio', ..., 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Grand Total'
    headers = df_cubo.iloc[1]
    print("Cubo Headers:", headers.tolist())
    
    # Filter for Mezquital
    mez_rows = df_cubo[df_cubo.apply(lambda row: row.astype(str).str.contains('Mezquital', case=False).any(), axis=1)]
    # Sum columns for Enero to Mayo
    months_cols = [i for i, h in enumerate(headers) if str(h) in ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo']]
    total_jan_may = mez_rows[months_cols].apply(pd.to_numeric, errors='coerce').sum().sum()
    print(f"Total doses Jan-May 2025 (Cubo): {total_jan_may}")
except Exception as e:
    print(f"Error extracting Cubo: {e}")

# 3. CSV - SRP-SR 2025 (May 2025 onwards)
print("\n--- EXTRACTING CSV DOSES ---")
try:
    df_csv = pd.read_csv(files['csv'], encoding='latin-1', sep=',')
    mez_csv = df_csv[df_csv['MUNICIPIO'].str.contains('MEZQUITAL', case=False, na=False)]
    
    # Age group distribution in CSV
    # Column mapping (approximate based on headers seen)
    groups = {
        '6-11m': ['SRP 6 A 11 MESES PRIMERA', 'SR 6 A 11 MESES PRIMERA'],
        '1y': ['SRP 1 ANIO  PRIMERA', 'SR 1 ANIO PRIMERA'],
        '18m': ['SRP 18 MESES SEGUNDA', 'SR 18 MESES SEGUNDA'],
        '2-12y': ['SRP 2 A 5 ANIOS PRIMERA', 'SRP 6 ANIOS PRIMERA', 'SRP 7 A 9 ANIOS PRIMERA', 'SRP 10 A 12 ANIOS PRIMERA',
                  'SRP 2 A 5 ANIOS SEGUNDA', 'SRP 6 ANIOS SEGUNDA', 'SRP 7 A 9 ANIOS SEGUNDA', 'SRP 10 A 12 ANIOS SEGUNDA',
                  'SR 2 A 5 ANIOS PRIMERA', 'SR 6 ANIOS PRIMERA', 'SR 7 A 9 ANIOS PRIMERA', 'SR 10 A 12 ANIOS PRIMERA',
                  'SR 2 A 5 ANIOS SEGUNDA', 'SR 6 ANIOS SEGUNDA', 'SR 7 A 9 ANIOS SEGUNDA', 'SR 10 A 12 ANIOS SEGUNDA'],
        '13-19y': ['SRP 13 A 19 ANIOS PRIMERA', 'SRP 13 A 19 ANIOS SEGUNDA', 'SRP 10 A 19 ANIOS PRIMERA', 'SRP 10 A 19 ANIOS SEGUNDA',
                   'SR 13 A 19 ANIOS PRIMERA', 'SR 13 A 19 ANIOS SEGUNDA', 'SR 10 A 19 ANIOS PRIMERA', 'SR 10 A 19 ANIOS SEGUNDA'],
        '20-39y': ['SRP 20 A 29 ANIOS PRIMERA', 'SRP 20 A 29 ANIOS SEGUNDA', 'SRP 30 A 39 ANIOS PRIMERA', 'SRP 30 A 39 ANIOS SEGUNDA',
                   'SR 20 A 29 ANIOS PRIMERA', 'SR 20 A 29 ANIOS SEGUNDA', 'SR 30 A 39 ANIOS PRIMERA', 'SR 30 A 39 ANIOS SEGUNDA'],
        '40-49y': ['SRP 40 A 49 ANIOS PRIMERA', 'SRP 40 A 49 ANIOS SEGUNDA',
                   'SR 40 A 49 ANIOS PRIMERA', 'SR 40 A 49 ANIOS SEGUNDA']
    }
    
    csv_distribution = {}
    for g, cols in groups.items():
        valid_cols = [c for c in cols if c in mez_csv.columns]
        val = mez_csv[valid_cols].apply(pd.to_numeric, errors='coerce').fillna(0).sum().sum()
        csv_distribution[g] = int(val)
    print("CSV Distribution:", csv_distribution)
except Exception as e:
    print(f"Error extracting CSV: {e}")
