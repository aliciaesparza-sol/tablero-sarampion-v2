import pandas as pd
import os

path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\CRONOGRAMAS DE VISITAS ESCUELAS'
files = os.listdir(path)

print(f"Found {len(files)} files.")

for f in files:
    if not f.endswith(('.xlsx', '.xls', '.csv')):
        continue
    
    file_path = os.path.join(path, f)
    print(f"\n{'='*50}")
    print(f"FILE: {f}")
    try:
        if f.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='latin1', nrows=5)
        else:
            df = pd.read_excel(file_path, nrows=5)
        
        print("Columns:", df.columns.tolist())
        print("\nFirst 2 rows:")
        print(df.head(2).to_string())
    except Exception as e:
        print(f"Error reading {f}: {e}")
