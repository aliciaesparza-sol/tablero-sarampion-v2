import pandas as pd

file_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\POBLACIÓN\POBLACION 2026\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx'

df = pd.read_excel(file_path, sheet_name='Durango')

# Let's inspect column headers (row 3 is where the municipality names seem to be)
mun_row = df.iloc[3].tolist()
print("Row 3 values (Municipalities):")
for idx, val in enumerate(mun_row):
    print(f"Index {idx}: {val}")

# Let's inspect the first column's unique values to see the structure of ages / sexes
print("\nFirst column values:")
first_col = df.iloc[:, 0].tolist()
for idx, val in enumerate(first_col):
    if pd.isna(val):
        continue
    # Print non-numeric or interesting values in the first column, plus some age samples
    if not isinstance(val, (int, float)) or idx < 10 or idx > 110:
        print(f"Row {idx}: {val} (type: {type(val)})")
