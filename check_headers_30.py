import pandas as pd

temp_excel = r"C:\Users\aicil\.gemini\antigravity\scratch\orig_temp.xlsx"

try:
    df = pd.read_excel(temp_excel, sheet_name="Concentrado", header=None)
    headers = df.iloc[2].tolist()
    for i in range(25, 45):
        if pd.notna(headers[i]):
            print(f"Col {i}: {headers[i]}")
except Exception as e:
    print(f"Error: {e}")
