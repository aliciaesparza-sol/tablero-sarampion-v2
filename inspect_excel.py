import pandas as pd

file1 = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\VPH25-26_TOP100PTES.xlsx"
file2 = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\CRONOGRAMA_INTEGRADO_VPH_2025_12abril2026.xlsx"

print("Columns in TOP100PTES:")
try:
    df1 = pd.read_excel(file1)
    print(df1.columns.tolist())
except Exception as e:
    print("Error reading file1:", e)

print("\nColumns in CRONOGRAMA_INTEGRADO:")
try:
    df2 = pd.read_excel(file2)
    print(df2.columns.tolist())
except Exception as e:
    print("Error reading file2:", e)
