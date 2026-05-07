import pandas as pd

temp_excel = r"C:\Users\aicil\.gemini\antigravity\scratch\orig_temp.xlsx"

try:
    df = pd.read_excel(temp_excel, sheet_name="Concentrado", header=None)
    print("Row 0 (Super-headers):")
    print(df.iloc[0, 25:65].tolist())
    print("\nRow 1 (Headers):")
    print(df.iloc[1, 25:65].tolist())
except Exception as e:
    print(f"Error: {e}")
