import pandas as pd
import os
import shutil

scratch = r"c:\Users\aicil\.gemini\antigravity\scratch"
ra_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\FORMATOS\FORMATOS CENSIA\BLOQUEO VACUNAL\FORMATO RESPUESTA RAPIDA.xlsx"
local = os.path.join(scratch, "temp_ra_inspect.xlsx")
shutil.copy2(ra_path, local)

xl = pd.ExcelFile(local)
df = xl.parse("ANEXO B", header=None, nrows=10)
print("--- HEADERS IN RA (ANEXO B) ---")
for i, row in df.iterrows():
    print(f"Row {i}: {row.tolist()}")
