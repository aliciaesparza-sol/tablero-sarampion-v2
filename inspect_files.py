import pandas as pd
import os

files = {
    'csv': r'c:\Descargas_SRP\SRP-SR-2025_10-04-2026 09-26-01.csv',
    'poblacion': r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO SARAMPION V2\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx',
    'cubo': r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\cubo_sis_consolidado-1.xlsx'
}

print("--- CSV HEADER ---")
try:
    df_csv_head = pd.read_csv(files['csv'], encoding='latin-1', sep=None, engine='python', nrows=0)
    print(df_csv_head.columns.tolist())
except Exception as e:
    print(f"Error reading CSV: {e}")

print("\n--- POBLACION SHEETS ---")
try:
    xl_pob = pd.ExcelFile(files['poblacion'])
    print(xl_pob.sheet_names)
except Exception as e:
    print(f"Error reading Poblacion: {e}")

print("\n--- CUBO SHEETS ---")
try:
    xl_cubo = pd.ExcelFile(files['cubo'])
    print(xl_cubo.sheet_names)
except Exception as e:
    print(f"Error reading Cubo: {e}")
