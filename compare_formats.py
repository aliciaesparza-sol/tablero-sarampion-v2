import pandas as pd
import os
import shutil

scratch_dir = r"c:\Users\aicil\.gemini\antigravity\scratch"
path1 = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\FORMATOS\FORMATOS CENSIA\BLOQUEO VACUNAL\FORMATO RESPUESTA RAPIDA.xlsx"
path2 = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\FORMATOS\FORMATOS CENSIA\BLOQUEO VACUNAL\Formato_Concentrado_Vacunacion_Sarampion.xlsx"

def dump_file(path, label):
    filename = os.path.basename(path)
    local_path = os.path.join(scratch_dir, "temp_" + filename)
    print(f"\n--- {label} ({filename}) ---")
    try:
        shutil.copy2(path, local_path)
        xl = pd.ExcelFile(local_path)
        for sheet in xl.sheet_names:
            print(f"Sheet: {sheet}")
            df = xl.parse(sheet, header=None, nrows=15)
            for i, row in df.iterrows():
                row_vals = [str(x).replace('\n', ' ').strip() for x in row.tolist()]
                if any(x != 'nan' and x != '' for x in row_vals):
                    print(f"Row {i}: {row_vals}")
    except Exception as e:
        print(f"Error: {e}")

dump_file(path1, "FORMATO A (ORIGEN)")
dump_file(path2, "FORMATO B (DESTINO)")
