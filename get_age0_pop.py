import pandas as pd

excel_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\POBLACIÓN\POBLACION 2026\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx"

try:
    df = pd.read_excel(excel_path, sheet_name='Durango', header=None)
    col_idx = 15
    hombres_idx = -1
    mujeres_idx = -1
    for i in range(len(df)):
        val = str(df.iloc[i, 0])
        if "Hombres" in val: hombres_idx = i
        if "Mujeres" in val: mujeres_idx = i
    
    # Age 0 is row hombres_idx + 1 and mujeres_idx + 1
    h0 = float(df.iloc[hombres_idx + 1, col_idx])
    m0 = float(df.iloc[mujeres_idx + 1, col_idx])
    print(f"Population Age 0: {h0 + m0}")
except Exception as e:
    print(f"Error: {e}")
