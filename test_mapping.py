import pandas as pd
import unicodedata

def normalize_name(name):
    if pd.isna(name): return ""
    name = str(name).strip().upper()
    # Remove accents
    name = "".join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    # Replace common issues
    name = name.replace('', 'N').replace('Ñ', 'N')
    return name

# Pop file
pop_path = r"C:/Users/aicil/OneDrive/Escritorio/PVU/SARAMPIÓN/COBERTURA DE VACUNACIÓN/TABLERO 3/Poblacion_municipio_edad_simple_y_sexo_Mexico_2026_CENJSIA_EGM.xlsx"
df_pop = pd.read_excel(pop_path, sheet_name='Durango', header=3)
pop_names = df_pop.iloc[0, 1:40].tolist()
pop_norm = {normalize_name(n): n for n in pop_names}

# Week file
week_path = r"C:/Users/aicil/OneDrive/Escritorio/PVU/SARAMPIÓN/COBERTURA POR MUNICIPIO Y SEMANA EPIDEMIOLÒGICA/COBERTURAS POR MUNICIPIO SRP Y SR 2025 12M,18M Y 6A POR SEMANA EPIDEMIOLOGICA.xlsx"
df_week = pd.read_excel(week_path, sheet_name='SE 53', header=5)
week_names = df_week.iloc[:, 0].tolist()
week_norm = {normalize_name(n): n for n in week_names}

# Compare
print("Missing in Pop file:")
for wn_norm, wn in week_norm.items():
    if wn_norm not in pop_norm and wn_norm != "TOTAL DURANGO" and wn_norm != "":
        print(f" - {wn}")

print("\nMissing in Week file:")
for pn_norm, pn in pop_norm.items():
    if pn_norm not in week_norm and pn_norm != "POBLACION TOTAL H Y M" and pn_norm != "":
        print(f" - {pn}")
