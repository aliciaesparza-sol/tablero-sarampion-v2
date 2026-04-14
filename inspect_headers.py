import pandas as pd
import os

path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\CRONOGRAMAS DE VISITAS ESCUELAS'
files = os.listdir(path)

for f in files:
    if not f.endswith(('.xlsx', '.xls')):
        continue
    
    file_path = os.path.join(path, f)
    print(f"\n{'='*50}")
    print(f"FILE: {f}")
    try:
        # Read first 20 rows to see where the data starts
        df = pd.read_excel(file_path, header=None, nrows=20)
        print(df.to_string())
    except Exception as e:
        print(f"Error reading {f}: {e}")
