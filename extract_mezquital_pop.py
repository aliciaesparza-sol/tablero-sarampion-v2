import pandas as pd

excel_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\POBLACIÓN\POBLACION 2026\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx"

try:
    df = pd.read_excel(excel_path, sheet_name='Durango', header=None)
    # Find "Mezquital"
    mask = df.apply(lambda row: row.astype(str).str.contains('Mezquital', case=False).any(), axis=1)
    matching_rows = df[mask]
    
    if not matching_rows.empty:
        idx = matching_rows.index[0]
        # Usually these files have rows for each age (0, 1, 2, ..., 100+)
        # Let's extract the rows starting from Mezquital and stop when we see the next municipality or end
        mez_data = df.iloc[idx:idx+110] # Assuming ~100 ages
        mez_data.to_csv("mezquital_population_raw.csv", index=False)
        print("Extracted Mezquital raw data to mezquital_population_raw.csv")
        print("First 5 rows:")
        print(mez_data.head())
    else:
        print("Mezquital not found.")

except Exception as e:
    print(f"Error: {e}")
