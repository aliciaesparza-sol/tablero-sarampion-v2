import pandas as pd

filepath = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\EXISTENCIAS SRP Y SR\EXISTENCIAS_SRP_SR_POR_DIA.xlsx"
xl = pd.ExcelFile(filepath)
df_res = xl.parse("Resumen ")
print("=== Resumen ===")
print(df_res.head(10).to_string())
df_det = xl.parse("Detalle por Jurisdicción")
print("\n=== Detalle por Jurisdicción ===")
print(df_det.head(10).to_string())
