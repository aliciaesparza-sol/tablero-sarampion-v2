import pandas as pd

file_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\BLOQUEOS VACUNALES\BLOQUEOS VACUNALES 2026\VACUNACIÓN MEZQUITAL 2026\Formato_Concentrado_Mezquital_2026_Con_Datos_Geograficos.xlsx"

try:
    df = pd.read_excel(file_path, sheet_name="Concentrado", header=None)
    print("Columnas 61, 62, 63 y 82 (Población):")
    # Row 2 is header, row 4 is data
    print(df.iloc[2:10, [61, 62, 63, 82]].to_string(index=False))

except Exception as e:
    print(f"Error: {e}")
