import pandas as pd

filepath = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\EXISTENCIAS SRP Y SR\EXISTENCIAS_DE_INSTITUCIONES_SRP_Y_SR.xlsx"
df = pd.read_excel(filepath, sheet_name="EXISTENCIAS DE INSTITUCIONES ")

df.head(50).to_csv(r"C:\Users\aicil\.gemini\antigravity\scratch\inst_data.csv", index=False)
