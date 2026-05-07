import pandas as pd

temp_excel = r"C:\Users\aicil\.gemini\antigravity\scratch\orig_temp.xlsx"

try:
    df = pd.read_excel(temp_excel, sheet_name="Concentrado", header=None)
    print("Columns 0-10 of first 5 data rows:")
    print(df.iloc[2:10, 0:10])
except Exception as e:
    print(f"Error: {e}")
