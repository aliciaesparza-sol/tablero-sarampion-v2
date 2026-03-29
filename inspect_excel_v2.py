import pandas as pd
import json

file_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\CAMPAÑA SARAMPIÓN 10 SEMANAS\Cobertura_SRP-SR_SSA_Durango_2026.xlsx'

try:
    xl = pd.ExcelFile(file_path)
    sheet_name = xl.sheet_names[0]
    df = xl.parse(sheet_name, header=None)
    
    # Drop rows and columns that are entirely NaN
    df = df.dropna(how='all').dropna(axis=1, how='all')
    
    # Convert to list of lists for easier reading
    rows = df.head(50).values.tolist()
    
    print(f"Sheet: {sheet_name}")
    print(f"Dimensions after dropping all-NaN: {df.shape}")
    
    for i, row in enumerate(rows):
        # Filter out NaN values from display
        clean_row = [str(v) if pd.notna(v) else "" for v in row]
        # Only print if row has some content
        if any(v != "" for v in clean_row):
            print(f"Row {i:2}: {' | '.join(clean_row)}")

except Exception as e:
    print(f"Error: {e}")
