import pandas as pd

def get_col_names(path):
    df = pd.read_excel(path, sheet_name='Concentrado', header=None)
    # The header seems to span multiple rows (2, 3, 4)
    print("Row 2:", df.iloc[2].tolist())
    print("Row 3:", df.iloc[3].tolist())

get_col_names(r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\BLOQUEOS VACUNALES\BLOQUEOS VACUNALES 2026\SAN FRANCISCO DE OCOTAN, MEZQUITAL_17.04.2026\san fco de ocotan Formato_Concentrado_Vacunacion_Sarampion-mezquital.xlsx")
