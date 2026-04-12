import pandas as pd
import os

files = {
    'csv': r'c:\Descargas_SRP\SRP-SR-2025_10-04-2026 09-26-01.csv',
    'poblacion': r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO SARAMPION V2\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx',
    'cubo': r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\cubo_sis_consolidado-1.xlsx'
}

# 1. Search for MEZQUITAL in Poblacion
print("--- SEARCHING MEZQUITAL IN POBLACION ---")
try:
    df_pob = pd.read_excel(files['poblacion'], sheet_name='Durango')
    # Find the row where 'MEZQUITAL' appears
    mez_rows = df_pob[df_pob.apply(lambda row: row.astype(str).str.contains('MEZQUITAL', case=False).any(), axis=1)]
    if not mez_rows.empty:
        print(f"Found MEZQUITAL at index: {mez_rows.index.tolist()}")
        # Usually, the data for a municipality follows the row where its name appears
        # I'll extract 100 rows from the first find to see the structure
        idx = mez_rows.index[0]
        sample = df_pob.iloc[idx:idx+100]
        # Save to file to inspect
        sample.to_csv(r'C:\Users\aicil\.gemini\antigravity\scratch\mezquital_poblacion_sample.csv', index=False)
    else:
        print("MEZQUITAL not found in Durango sheet.")
except Exception as e:
    print(f"Error reading Poblacion: {e}")

# 2. Search for MEZQUITAL in Cubo
print("\n--- SEARCHING MEZQUITAL IN CUBO ---")
try:
    df_cubo = pd.read_excel(files['cubo'], sheet_name='Cubo SIS Consolidado')
    mez_cubo = df_cubo[df_cubo.apply(lambda row: row.astype(str).str.contains('MEZQUITAL', case=False).any(), axis=1)]
    if not mez_cubo.empty:
        print(f"Found MEZQUITAL in Cubo at index: {mez_cubo.index.tolist()}")
        print(mez_cubo)
    else:
        print("MEZQUITAL not found in Cubo.")
except Exception as e:
    print(f"Error reading Cubo: {e}")

# 3. CSV Filter for MEZQUITAL
print("\n--- SEARCHING MEZQUITAL IN CSV ---")
try:
    df_csv = pd.read_csv(files['csv'], encoding='latin-1', sep=None, engine='python')
    mez_csv = df_csv[df_csv['MUNICIPIO'].str.contains('MEZQUITAL', case=False, na=False)]
    print(f"Found {len(mez_csv)} records for MEZQUITAL in CSV.")
    # Sum doses
    doses_cols = [c for c in df_csv.columns if 'SRP' in c or 'SR ' in c]
    total_doses_csv = mez_csv[doses_cols].sum().sum()
    print(f"Total doses in CSV for MEZQUITAL: {total_doses_csv}")
except Exception as e:
    print(f"Error reading CSV: {e}")
