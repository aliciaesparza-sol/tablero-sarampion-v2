import pandas as pd
import json

files = [
    r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\EXISTENCIAS SRP Y SR\EXISTENCIAS_SRP_SR_POR_DIA.xlsx",
    r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\INFORME\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS 10.03.2026.xlsx"
]

out = {}
for f in files:
    try:
        xl = pd.ExcelFile(f)
        out[f] = {}
        for s in xl.sheet_names:
            try:
                df = xl.parse(s, nrows=2)
                out[f][s] = list(df.columns)
            except Exception as e:
                out[f][s] = "Error: " + str(e)
    except Exception as e:
        out[f] = "Error: " + str(e)

with open('schema.json', 'w', encoding='utf-8') as fh:
    json.dump(out, fh, indent=2, ensure_ascii=False)
