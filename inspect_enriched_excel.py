import pandas as pd

excel_path = r"C:\Users\aicil\.gemini\antigravity\scratch\Formato_Concentrado_Mezquital_2026_Updated.xlsx"

try:
    df = pd.read_excel(excel_path, sheet_name="Concentrado", header=None)
    # The localities start at row 4 (index 3). 
    # Let's find the columns for Localidad and Doses.
    # Previous analysis said Localidad is column 4 (index 4).
    # Doses was likely in one of the columns.
    
    # Let's show the first few rows and columns to identify
    print(df.iloc[2:10, 0:10])
    
    # We also enriched it with population and coverage.
    # Let's see the last few columns
    print("\n--- LAST COLUMNS ---")
    print(df.iloc[2:10, -5:])

except Exception as e:
    print(f"Error: {e}")
