import pandas as pd

excel_path = r"C:\Users\aicil\.gemini\antigravity\scratch\Formato_Concentrado_Mezquital_2026_Updated.xlsx"

try:
    df = pd.read_excel(excel_path, sheet_name="Concentrado", header=None)
    # Row 2 (index 2) usually has headers
    headers = df.iloc[2].tolist()
    for i, h in enumerate(headers):
        if pd.notna(h):
            print(f"Col {i}: {h}")
            
except Exception as e:
    print(f"Error: {e}")
