import pandas as pd
import os
import shutil

scratch_dir = r"c:\Users\aicil\.gemini\antigravity\scratch"
paths = [
    r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\FORMATOS\FORMATOS CENSIA\BLOQUEO VACUNAL\FORMATO RESPUESTA RAPIDA.xlsx",
    r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\FORMATOS\FORMATOS CENSIA\BLOQUEO VACUNAL\Formato_Concentrado_Vacunacion_Sarampion.xlsx"
]

print("--- Extraction Report ---")
for path in paths:
    filename = os.path.basename(path)
    local_path = os.path.join(scratch_dir, filename)
    print(f"\nProcessing File: {filename}")
    
    try:
        # Try to copy it locally in case of file locks
        shutil.copy2(path, local_path)
        xl = pd.ExcelFile(local_path)
        for sheet_name in xl.sheet_names:
            print(f"  Sheet: {sheet_name}")
            df = xl.parse(sheet_name, header=None, nrows=20)
            
            # Print the first few rows to visually inspect headers
            for i, row in df.iterrows():
                # Filter out all-nans for cleaner reading
                row_list = [str(x).strip() for x in row.tolist()]
                # If there's at least one meaningful string, print it
                if any(x != 'nan' and len(x) > 0 for x in row_list):
                    print(f"    Row {i}: {row_list}")
    except Exception as e:
        print(f"  Error: {e}")
