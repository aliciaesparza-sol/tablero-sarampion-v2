import pandas as pd

excel_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\POBLACIÓN\POBLACION 2026\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx"

try:
    # Read first sheet
    xls = pd.ExcelFile(excel_path)
    print(f"Sheets: {xls.sheet_names}")
    
    df = pd.read_excel(excel_path, sheet_name=0, nrows=10)
    print("--- HEADERS ---")
    print(df.columns.tolist())
    print("\n--- FIRST ROWS ---")
    print(df.head(10))

except Exception as e:
    print(f"Error: {e}")
