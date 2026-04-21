import pandas as pd

def read_concentrado(path):
    print(f"--- Reading Concentrado: {path} ---")
    df = pd.read_excel(path, sheet_name='Concentrado', header=None)
    # Fill NaNs with empty string for better visibility
    df = df.fillna('')
    print(df.to_string())

read_concentrado(r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\BLOQUEOS VACUNALES\BLOQUEOS VACUNALES 2026\SAN FRANCISCO DE OCOTAN, MEZQUITAL_17.04.2026\san fco de ocotan Formato_Concentrado_Vacunacion_Sarampion-mezquital.xlsx")
