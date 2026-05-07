import pandas as pd
import numpy as np

file_path = r"C:\Users\aicil\.gemini\antigravity\scratch\Formato_Concentrado_Mezquital_2026_Updated.xlsx"

try:
    df = pd.read_excel(file_path, sheet_name="Concentrado", header=None)
    df = df.astype(object)
    
    # Ensure columns up to 83
    for c in range(df.shape[1], 84):
        df[c] = None
    
    df.at[2, 82] = "Poblacion Total (INEGI 2020)"
    df.at[2, 83] = "Alcance (%)"
    
    # Recalculate Alcance
    for i in range(3, len(df)):
        try:
            total_doses = pd.to_numeric(df.iloc[i, 61], errors='coerce')
            poblacion = pd.to_numeric(df.iloc[i, 82], errors='coerce')
            if pd.notna(total_doses) and pd.notna(poblacion) and poblacion > 0:
                df.at[i, 83] = total_doses / poblacion
            else:
                df.at[i, 83] = 0
        except:
            df.at[i, 83] = 0

    with pd.ExcelWriter(file_path) as writer:
        df.to_excel(writer, sheet_name="Concentrado", index=False, header=False)
    print("Excel file fixed with Alcance column.")

except Exception as e:
    print(f"Error: {e}")
