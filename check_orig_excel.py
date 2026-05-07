import pandas as pd

orig_excel = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\BLOQUEOS VACUNALES\BLOQUEOS VACUNALES 2026\VACUNACIÓN MEZQUITAL 2026\Formato_Concentrado_Vacunacion_Sarampion_Mezquital_2026xlsx(Recuperado automáticamente).xlsx"

try:
    df = pd.read_excel(orig_excel, sheet_name="Concentrado", header=None)
    # Check headers in row 2
    headers = df.iloc[2].tolist()
    print("Headers in original file:")
    for i, h in enumerate(headers):
        if pd.notna(h):
            print(f"Col {i}: {h}")
            
    # Sample data for AMOLES (usually first locality)
    # Find AMOLES in column 4
    for i in range(len(df)):
        if "AMOLES" in str(df.iloc[i, 4]):
            print(f"\nData for AMOLES (Row {i}):")
            print(f"Col 34 (TOTAL): {df.iloc[i, 34]}")
            print(f"Col 53 (TOTAL): {df.iloc[i, 53]}")
            print(f"Col 61 (TOTAL): {df.iloc[i, 61]}")
            print(f"Col 78 (TOTAL): {df.iloc[i, 78]}")
            break

except Exception as e:
    print(f"Error: {e}")
