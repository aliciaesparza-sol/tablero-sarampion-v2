import pandas as pd
import sys

file_path = r"C:\Users\aicil\.gemini\antigravity\scratch\temp_file.xlsx"

try:
    # Read the excel file
    xls = pd.ExcelFile(file_path)
    print(f"Sheets found: {xls.sheet_names}")
    
    for sheet_name in xls.sheet_names:
        print(f"\n--- Sheet: {sheet_name} ---")
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Columns: {df.columns.tolist()[:10]}...")
        print("First 5 rows:")
        print(df.head(5))
        
        # Look for locality column
        locality_col = None
        for col in df.columns:
            if any(term in str(col).upper() for term in ['LOCALIDAD', 'COMUNIDAD', 'NOMBRE']):
                locality_col = col
                break
        
        if locality_col:
            print(f"Potential locality column: {locality_col}")
        
except Exception as e:
    print(f"Error: {e}")

except Exception as e:
    print(f"Error: {e}")
