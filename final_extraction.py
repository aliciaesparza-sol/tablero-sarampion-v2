import pandas as pd
import os

scratch = r"c:\Users\aicil\.gemini\antigravity\scratch"
ra_path = os.path.join(scratch, 'temp_ra.xlsx')
conc_path = os.path.join(scratch, 'temp_conc.xlsx')

def get_sheet_data(path, sheet_name):
    xl = pd.ExcelFile(path)
    df = xl.parse(sheet_name, header=None, nrows=15)
    result = []
    for i, row in df.iterrows():
        clean_row = [str(x).strip() for x in row.tolist()]
        # Check if line has any data
        if any(x != 'nan' and x != '' for x in clean_row):
            result.append((i, clean_row))
    return result

print("### ANALISIS DE FORMATO RESPUESTA RAPIDA ###")
try:
    data_ra = get_sheet_data(ra_path, 'ANEXO B')
    for i, row in data_ra:
        print(f"Row {i}: {row}")
except Exception as e:
    print(f"Error RA: {e}")

print("\n### ANALISIS DE FORMATO CONCENTRADO ###")
try:
    xl_conc = pd.ExcelFile(conc_path)
    for s in xl_conc.sheet_names:
        print(f"\nSheet: {s}")
        data_c = get_sheet_data(conc_path, s)
        for i, row in data_c:
            print(f"  Row {i}: {row}")
except Exception as e:
    print(f"Error CONC: {e}")
