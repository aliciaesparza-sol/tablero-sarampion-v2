import pandas as pd
import sys

# Reconfigure stdout to use utf-8 to avoid CP1252 encoding errors in Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:\Users\aicil\.gemini\antigravity-ide\scratch\temp_cobertura.xlsx'
xl = pd.ExcelFile(file_path)

for idx, sheet in enumerate(xl.sheet_names):
    print(f"\nSheet Index {idx}: '{sheet}'")
    df = pd.read_excel(file_path, sheet_name=sheet, header=None)
    print(f"Shape: {df.shape}")
    print("Row 0:", list(df.iloc[0].dropna())[:3])
    print("Row 1:", list(df.iloc[1].dropna())[:3])
    print("Row 3:", list(df.iloc[3].dropna())[:15])
    print("Row 4:", list(df.iloc[4].dropna())[:15])
