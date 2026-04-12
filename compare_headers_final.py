import pandas as pd
import os

scratch = r"c:\Users\aicil\.gemini\antigravity\scratch"
ra_path = os.path.join(scratch, 'temp_ra.xlsx')
conc_path = os.path.join(scratch, 'temp_conc.xlsx')

def get_headers(path, sheet_name):
    try:
        xl = pd.ExcelFile(path)
        df = xl.parse(sheet_name, header=None, nrows=30)
        # Search for headers - usually the row with most strings
        for i, row in df.iterrows():
            row_vals = [str(x).strip() for x in row.tolist()]
            non_empty = [x for x in row_vals if x != 'nan' and x != '']
            if len(non_empty) > 10: # Likely the header row
                return row_vals
        return []
    except Exception as e:
        return [f"Error: {e}"]

h_ra = get_headers(ra_path, 'ANEXO B')
h_conc = get_headers(conc_path, 'Formato bloqueo barrido')

print("--- HEADERS IN RESPUESTA RAPIDA (RA) ---")
for i, h in enumerate(h_ra):
    print(f"{i}: {h}")

print("\n--- HEADERS IN CONCENTRADO (CONC) ---")
for i, h in enumerate(h_conc):
    print(f"{i}: {h}")

# Find missing in CONC
missing = []
for h in h_ra:
    if h != 'nan' and h != '' and h not in h_conc:
        missing.append(h)

print("\n--- POTENTIALLY MISSING FIELDS ---")
for m in missing:
    print(f"- {m}")
