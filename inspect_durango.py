import pandas as pd

excel_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\POBLACIÓN\POBLACION 2026\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx"

try:
    df = pd.read_excel(excel_path, sheet_name='Durango', nrows=20)
    print("--- DURANGO SHEET HEADERS/ROWS ---")
    print(df.head(20))

except Exception as e:
    print(f"Error: {e}")
