import pandas as pd

file_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\BLOQUEOS VACUNALES\BLOQUEOS VACUNALES 2026\VACUNACIÓN MEZQUITAL 2026\Formato_Concentrado_Mezquital_2026_Con_Datos_Geograficos.xlsx"

try:
    df = pd.read_excel(file_path, sheet_name="Concentrado", header=None)
    # Show first 15 rows and columns with data
    print("Primeras 15 filas del archivo actualizado:")
    # Selecting columns: Localidad (4), CP (7), Lat (8), Lon (9), Pob (82)
    display_cols = [3, 4, 7, 8, 9, 82]
    # Filter only existing columns
    display_cols = [c for c in display_cols if c < df.shape[1]]
    
    print(df.iloc[2:15, display_cols].to_string(index=False))

except Exception as e:
    print(f"Error: {e}")
