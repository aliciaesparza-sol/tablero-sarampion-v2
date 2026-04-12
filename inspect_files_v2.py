import pandas as pd
import os

files = {
    'csv': r'c:\Descargas_SRP\SRP-SR-2025_10-04-2026 09-26-01.csv',
    'poblacion': r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO SARAMPION V2\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx',
    'cubo': r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\cubo_sis_consolidado-1.xlsx'
}

print("--- CSV HEADERS AND SAMPLE ---")
try:
    # Use semicolon as separator for these government CSVs usually
    df_csv = pd.read_csv(files['csv'], encoding='latin-1', sep=None, engine='python', nrows=5)
    print(df_csv.columns.tolist())
    # Find records for MEZQUITAL if exists
    if 'MUNICIPIO' in df_csv.columns:
        print("MUNICIPIO column found.")
except Exception as e:
    print(f"Error reading CSV: {e}")

print("\n--- POBLACION DURANGO SAMPLE ---")
try:
    # Read Durango sheet. Skip some rows usually as there's a header.
    df_pob = pd.read_excel(files['poblacion'], sheet_name='Durango', nrows=10)
    print("Columns:", df_pob.columns.tolist())
    print("Top rows:")
    print(df_pob.head(5))
except Exception as e:
    print(f"Error reading Poblacion: {e}")

print("\n--- CUBO SIS CONSOLIDADO SAMPLE ---")
try:
    df_cubo = pd.read_excel(files['cubo'], sheet_name='Cubo SIS Consolidado', nrows=10)
    print("Columns:", df_cubo.columns.tolist())
    print("Top rows:")
    print(df_cubo.head(5))
except Exception as e:
    print(f"Error reading Cubo: {e}")
