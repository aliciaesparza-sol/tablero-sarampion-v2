import pandas as pd, sys
excel_path = r"C:/Users/aicil/OneDrive/Escritorio/PVU/ANEXOS DGO/VACUNACIÓN ANEXOS FINAL.xlsx"
try:
    df = pd.read_excel(excel_path, engine='openpyxl')
except Exception as e:
    sys.exit(f'Error reading Excel: {e}')
print('Columnas:', list(df.columns))
print('Primeras 5 filas:')
print(df.head())
