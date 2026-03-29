import pandas as pd
import sys

file_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\CAMPAÑA SARAMPIÓN 10 SEMANAS\Cobertura_SRP-SR_SSA_Durango_2026.xlsx'

try:
    # Read all sheets (if there are multiple)
    xl = pd.ExcelFile(file_path)
    print(f"Sheet names: {xl.sheet_names}")
    
    for sheet_name in xl.sheet_names:
        print(f"\n--- Sheet: {sheet_name} ---")
        df = xl.parse(sheet_name, header=None)
        
        # Look for the first row that has 'MUNICIPIO' or similar terms
        for r_idx, row in df.iterrows():
            row_values = [str(v).strip() for v in row if pd.notna(v)]
            if any('MUNICIPIO' in str(v).upper() for v in row_values):
                print(f"Found potential header at row {r_idx}: {row_values}")
                # Print a few rows after this
                print("\nNext 5 rows:")
                print(df.iloc[r_idx:r_idx+6, :15].to_string())
                break
        else:
            # If no header found, print first 10 rows
            print("No 'MUNICIPIO' found. Printing first 10 rows:")
            print(df.head(10).iloc[:, :15].to_string())

except Exception as e:
    print(f"Error: {e}")
