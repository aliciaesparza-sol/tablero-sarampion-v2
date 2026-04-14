import pandas as pd

file2 = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\CRONOGRAMA_INTEGRADO_VPH_2025_12abril2026.xlsx"
df2 = pd.read_excel(file2)
print("Head of CRONOGRAMA_INTEGRADO:")
print(df2.head())
print("\nTypes:")
print(df2.dtypes)
