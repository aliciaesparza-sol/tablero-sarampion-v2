import pandas as pd

new_crono_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\CRONOGRAMAS DE VISITAS ESCUELAS\CRONOGRAMA DE ESCUELAS JURISDCCION 2.xlsx"

try:
    df_new = pd.read_excel(new_crono_path)
    print("Primeras 20 filas de PRIMARIAS:")
    for val in df_new['PRIMARIAS'].dropna().head(20):
        print(f" - {val}")
        
    print("\nPrimeras 20 filas de PRIMARIAS.1:")
    for val in df_new['PRIMARIAS.1'].dropna().head(20):
        print(f" - {val}")

except Exception as e:
    print(f"Error: {e}")
