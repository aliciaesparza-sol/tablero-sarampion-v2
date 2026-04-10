import pandas as pd
import numpy as np

excel_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO 3\Cobertura_Sarampion_Durango_Municipio_04abril2026.xlsx"
csv_path = r"c:\Descargas_SRP\SRP-SR-2025_08-04-2026 02-31-03.csv"
output_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO 3\DATOS_CORREGIDOS_TABLERO.xlsx"

# 1. Leer CSV y sacar dosis nominas por municipio
df_csv = pd.read_csv(csv_path, sep=";", encoding="latin1", low_memory=False)
df_csv["_dosis"] = df_csv[["SRP  PRIMERA TOTAL", "SRP SEGUNDA TOTAL", "SR PRIMERA TOTAL", "SR SEGUNDA TOTAL"]].sum(axis=1)

# Normalizar nombres de municipio (mayúsculas) para hacer el merge
df_csv["MUNICIPIO_NORM"] = df_csv["MUNICIPIO"].astype(str).str.strip().str.upper()
dosis_nominales = df_csv.groupby("MUNICIPIO_NORM")["_dosis"].sum().reset_index()
dosis_nominales.rename(columns={"_dosis": "Nominal Jun-Abril"}, inplace=True)

# 2. Leer Excel original
import shutil
shutil.copy2(excel_path, "temp_excel2.xlsx")
df_excel = pd.read_excel("temp_excel2.xlsx", header=7)

# Renombrar columnas para usar
df_excel.rename(columns={
    "Municipio": "Municipio",
    "Universo\n2026": "Universo 2026",
    "Meta\nSect.": "Meta Sect.",
    "Cubos\nEne-May 25": "Cubos Ene-May 25"
}, inplace=True)

# Limpiar municipio para cruzar
df_excel["MUNICIPIO_NORM"] = df_excel["Municipio"].astype(str).str.strip().str.upper()

# Normalizar 'Pueblo Nuevo' si está como 'Pueblo Nuevo dgo' en CSV
dosis_nominales['MUNICIPIO_NORM'] = dosis_nominales['MUNICIPIO_NORM'].replace({'PUEBLO NUEVO DGO': 'PUEBLO NUEVO'})

# Cruzar
df_merged = pd.merge(df_excel, dosis_nominales, on="MUNICIPIO_NORM", how="left")
df_merged["Nominal Jun-Abril"] = df_merged["Nominal Jun-Abril"].fillna(0).astype(int)

# Crear nuevo DF con la estructura solicitada
df_final = pd.DataFrame()
df_final["Municipio"] = df_merged["Municipio"]
df_final["Universo 2026"] = df_merged["Universo 2026"].fillna(0).astype(int)
df_final["% Meta"] = (df_merged["Meta Sect."] / df_merged["Universo 2026"]).fillna(0)
df_final["Meta Sect."] = df_merged["Meta Sect."].fillna(0).astype(int)
df_final["Cubos Ene-May 25"] = df_merged["Cubos Ene-May 25"].fillna(0).astype(int)
df_final["Nominal Jun-Abril"] = df_merged["Nominal Jun-Abril"]
df_final["Total Dosis"] = df_final["Cubos Ene-May 25"] + df_final["Nominal Jun-Abril"]
df_final["Pendientes"] = df_final["Meta Sect."] - df_final["Total Dosis"]

# El cob vs meta
df_final["Cob. vs Meta (%)"] = (df_final["Total Dosis"] / df_final["Meta Sect."]).fillna(0)

# Semáforo
def get_semaforo(val):
    if val >= 0.95: return "✅ META ALCANZADA"
    elif val >= 0.80: return "🟢 BUENA COBERTURA"
    elif val >= 0.50: return "🟡 EN PROCESO"
    elif val >= 0.25: return "🟠 BAJA COBERTURA"
    else: return "🔴 CRÍTICO"

df_final["Semáforo"] = df_final["Cob. vs Meta (%)"].apply(get_semaforo)

# Ordenar columnas a como vienen en la imagen:
cols = ["Municipio", "Universo 2026", "% Meta", "Meta Sect.", "Cubos Ene-May 25", "Nominal Jun-Abril", "Total Dosis", "Pendientes", "Semáforo", "Cob. vs Meta (%)"]
df_final = df_final[cols]

# Eliminar fila vacía si municipio es nan
df_final = df_final[df_final["Municipio"].notna() & (df_final["Municipio"] != "nan")]

# Formatear el excel con openpyxl usando to_excel
with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
    df_final.to_excel(writer, index=False, sheet_name='Datos Corregidos')
    workbook = writer.book
    worksheet = writer.sheets['Datos Corregidos']
    
    # Formato %
    pct_fmt = workbook.add_format({'num_format': '0.0%'})
    num_fmt = workbook.add_format({'num_format': '#,##0'})
    
    worksheet.set_column('B:B', 12, num_fmt)
    worksheet.set_column('C:C', 10, pct_fmt)
    worksheet.set_column('D:H', 15, num_fmt)
    worksheet.set_column('I:I', 20)
    worksheet.set_column('J:J', 15, pct_fmt)

print(f"Éxito guardado en {output_path}")
