import pandas as pd

new_crono_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\CRONOGRAMAS DE VISITAS ESCUELAS\CRONOGRAMA DE ESCUELAS JURISDCCION 2.xlsx"

try:
    df_new = pd.read_excel(new_crono_path)
    print("Columns in new cronograma:")
    print(df_new.columns.tolist())
    print("\nHead:")
    print(df_new.head())
except Exception as e:
    print(f"Error: {e}")
