import pandas as pd

file_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\BLOQUEOS VACUNALES\BLOQUEOS VACUNALES 2026\VACUNACIÓN MEZQUITAL 2026\Formato_Concentrado_Mezquital_2026_Con_Datos_Geograficos.xlsx"

try:
    df = pd.read_excel(file_path, sheet_name="Concentrado", header=None)
    print("Primeras filas con Alcance (%):")
    # Columns: Localidad (4), Total Doses (61), Population (82), Alcance (83)
    print(df.iloc[2:15, [4, 61, 82, 83]].to_string(index=False))

except Exception as e:
    print(f"Error: {e}")
