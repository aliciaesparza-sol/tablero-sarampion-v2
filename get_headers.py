import pandas as pd

def get_headers(path, sheet_name):
    print(f"--- Headers for: {path} [{sheet_name}] ---")
    df = pd.read_excel(path, sheet_name=sheet_name, header=None)
    # Print the first 10 rows to see where headers might be
    print(df.head(15))

get_headers(r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\FORMATOS\FORMATOS CENSIA\BLOQUEO VACUNAL\FORMATO RESPUESTA RAPIDA.xlsx", "ANEXO B")
