import pandas as pd
import numpy as np

file_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\BLOQUEOS VACUNALES\BLOQUEOS VACUNALES 2026\VACUNACIÓN MEZQUITAL 2026\Formato_Concentrado_Mezquital_2026_Con_Datos_Geograficos.xlsx"
output_path = file_path # Overwrite or same path

try:
    # Load with sheet name
    df = pd.read_excel(file_path, sheet_name="Concentrado", header=None)
    df = df.astype(object)
    
    # Add new column 83: Alcance (%)
    if df.shape[1] <= 83:
        df[83] = None
    
    # Set Header
    df.at[2, 83] = "Alcance (%)"
    
    # Iterate from row 3 (data)
    for i in range(3, len(df)):
        try:
            total_doses = df.iloc[i, 61]
            poblacion = df.iloc[i, 82]
            
            # Convert to numeric
            doses = pd.to_numeric(total_doses, errors='coerce')
            pob = pd.to_numeric(poblacion, errors='coerce')
            
            if pd.notna(doses) and pd.notna(pob) and pob > 0:
                alcance = (doses / pob) * 100
                df.at[i, 83] = round(alcance, 2)
            else:
                df.at[i, 83] = 0
        except Exception:
            df.at[i, 83] = 0

    print(f"Saving updated file to {output_path}...")
    with pd.ExcelWriter(output_path) as writer:
        df.to_excel(writer, sheet_name="Concentrado", index=False, header=False)
    print("Done!")

except Exception as e:
    print(f"Error: {e}")
