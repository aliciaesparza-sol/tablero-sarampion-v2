import pandas as pd

excel_path = r"C:/Users/aicil/OneDrive/Escritorio/PVU/ANEXOS DGO/VACUNACIÓN ANEXOS FINAL.xlsx"

try:
    df = pd.read_excel(excel_path)
    print('Column names:', list(df.columns))
    print('First 5 rows:')
    print(df.head())
except Exception as e:
    print('Error reading Excel file:', e)
