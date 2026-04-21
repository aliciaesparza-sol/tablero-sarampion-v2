import pandas as pd

def inspect_pfam(path):
    print(f"--- Inspecting: {path} ---")
    xlsx = pd.ExcelFile(path)
    print(f"Sheets: {xlsx.sheet_names}")
    for sheet in xlsx.sheet_names:
        print(f"\nSheet: {sheet}")
        df = pd.read_excel(path, sheet_name=sheet, header=None)
        print("First 15 rows:")
        print(df.head(15).to_string())

inspect_pfam(r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\MICRO PFAM2025.xlsx")
