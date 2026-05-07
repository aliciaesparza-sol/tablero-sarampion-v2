import pandas as pd

excel_path = r"C:\Users\aicil\.gemini\antigravity\scratch\Formato_Concentrado_Mezquital_2026_Updated.xlsx"

try:
    df = pd.read_excel(excel_path, sheet_name="Concentrado", header=None)
    print(f"Shape: {df.shape}")
    print(f"Columns 82, 83: {df.iloc[2, 82:84].tolist()}")
    
    data = []
    # Use actual column count
    pob_col = 82
    alcance_col = 83
    doses_col = 61
    loc_col = 4
    
    for i in range(4, len(df)):
        loc = df.iloc[i, loc_col]
        if pd.isna(loc): continue
        doses = df.iloc[i, doses_col]
        pob = df.iloc[i, pob_col]
        alcance = df.iloc[i, alcance_col]
        if pd.notna(alcance) and isinstance(alcance, (int, float)) and alcance > 0:
            data.append({
                'Localidad': loc,
                'Dosis': doses,
                'Poblacion': pob,
                'Alcance': alcance
            })
            
    print("--- LOCALITY DATA (EXCEL) ---")
    for item in data:
        print(f"{item['Localidad']} | {item['Dosis']} | {item['Poblacion']} | {item['Alcance']:.2%}")

except Exception as e:
    print(f"Error: {e}")
