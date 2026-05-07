import pandas as pd

temp_excel = r"C:\Users\aicil\.gemini\antigravity\scratch\orig_temp.xlsx"

try:
    df = pd.read_excel(temp_excel, sheet_name="Concentrado", header=None)
    # Filter for LAS JOYAS
    mask = df.iloc[:, 4].astype(str).str.contains("LAS JOYAS", case=False)
    joyas_rows = df[mask]
    print("--- ROWS FOR LAS JOYAS ---")
    print(joyas_rows.iloc[:, [0, 1, 4, 61]]) # Inst, Semana?, Loc, Total
    
except Exception as e:
    print(f"Error: {e}")
