import pandas as pd
import sys

def inspect_excel(path):
    print(f"--- Inspecting: {path} ---")
    try:
        # Try to read the first sheet to see structure
        xlsx = pd.ExcelFile(path)
        print(f"Sheets: {xlsx.sheet_names}")
        for sheet_name in xlsx.sheet_names:
            print(f"\nSheet: {sheet_name}")
            df = pd.read_excel(path, sheet_name=sheet_name, header=None)
            print("First 10 rows:")
            print(df.head(10))
    except Exception as e:
        print(f"Error reading {path}: {e}")

inspect_excel(r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\FORMATOS\FORMATOS CENSIA\BLOQUEO VACUNAL\FORMATO RESPUESTA RAPIDA.xlsx")
inspect_excel(r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\BLOQUEOS VACUNALES\BLOQUEOS VACUNALES 2026\SAN FRANCISCO DE OCOTAN, MEZQUITAL_17.04.2026\san fco de ocotan Formato_Concentrado_Vacunacion_Sarampion-mezquital.xlsx")
