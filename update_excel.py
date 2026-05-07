import pandas as pd
import numpy as np
import unicodedata

# Files
user_excel = r"C:\Users\aicil\.gemini\antigravity\scratch\temp_file.xlsx"
inegi_csv = r"C:\Users\aicil\.gemini\antigravity\scratch\iter_durango\iter_10_cpv2020\conjunto_de_datos\conjunto_de_datos_iter_10CSV20.csv"
output_excel = r"C:\Users\aicil\.gemini\antigravity\scratch\Formato_Concentrado_Mezquital_2026_Updated.xlsx"

def normalize(s):
    if not isinstance(s, str): return ""
    s = s.upper().strip()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s

# Load INEGI data
print("Loading INEGI data...")
inegi_df = pd.read_csv(inegi_csv, dtype={'MUN': str, 'LOC': str})
# Filter for Mezquital (MUN 014)
mez_inegi = inegi_df[inegi_df['MUN'] == '014'].copy()
mez_inegi['NORM_LOC'] = mez_inegi['NOM_LOC'].apply(normalize)
mez_inegi = mez_inegi[mez_inegi['LOC'] != '0000']

inegi_map = {}
for idx, row in mez_inegi.iterrows():
    inegi_map[row['NORM_LOC']] = {
        'pob': row['POBTOT'],
        'lat': row['LATITUD'],
        'lon': row['LONGITUD']
    }

# Zip Code Data
zip_map = {
    "AGUA CALIENTE": "34994", "AGUACATES": "34983", "AGUACATES(ANGOSTURA)": "34983",
    "AMOLES": "34973", "ARMADILLO": "34985", "ARMADILLOS": "34985",
    "ARROYO HONDO": "34973", "BAJIO Y CENTRO": "34985", "BAJIO": "34985",
    "BERENJENAS": "34973", "BOTIJAS": "34973", "BUENAVISTA": "34973",
    "CARBONERAS": "34973", "CEBOLLAS": "34986", "CEBOLLAS DE MILPILLAS": "34986",
    "CERRO BLANCO": "34973", "CERRO BOLILLO": "34973", "CERRO DE LAS PALOMAS": "34983",
    "CIHUACORA": "34970", "COLOMOS": "34970", "CUMBRES": "34973",
    "ENRAMADAS": "34973", "GUACAMAYA": "34973", "GUYAVITOS": "34973",
    "HUAZAMOTITA": "34994", "LA ESCONDIDA": "34973", "LA GUAJOLOTA": "34970",
    "LAS AGUILILLAS": "34973", "LAS JOYAS": "34977", "LOS ARQUITOS": "34996",
    "LOS BANCOS": "34973", "MESA DEL LLANO": "34970", "PINO PARADO": "34986",
    "POTREROS": "34973", "SAN MANUEL": "34973", "STA MA. DE OCOTAN": "34985",
    "SANTA MARIA DE OCOTAN": "34985", "TEPALCATE": "34973", "TOMATES": "34973",
    "TRES LAGUNAS": "34996", "ZAPOTES": "34973"
}

# Load User Excel
print("Loading User Excel...")
df_user = pd.read_excel(user_excel, sheet_name="Concentrado", header=None)
df_user = df_user.astype(object)

# Ensure enough columns
max_col = 82
for c in range(df_user.shape[1], max_col + 1):
    df_user[c] = None

print("Updating rows...")
df_user.at[2, 82] = "Poblacion Total (INEGI 2020)"
df_user.at[0, 0] = "FUENTE: INEGI (Censo 2020 - ITER) y SEPOMEX (Correos de México)"

for i in range(3, len(df_user)):
    loc_raw = df_user.iloc[i, 4]
    if pd.isna(loc_raw): continue
    loc_norm = normalize(str(loc_raw))
    data = inegi_map.get(loc_norm)
    if not data:
        for key in inegi_map:
            if loc_norm in key or key in loc_norm:
                data = inegi_map[key]
                break
    if data:
        df_user.at[i, 8] = data['lat']
        df_user.at[i, 9] = data['lon']
        df_user.at[i, 82] = data['pob']
    z = zip_map.get(loc_norm)
    if not z:
        for key in zip_map:
            if loc_norm in key or key in loc_norm:
                z = zip_map[key]
                break
    if z:
        df_user.at[i, 7] = z

print(f"Saving updated file to {output_excel} with sheet name 'Concentrado'...")
with pd.ExcelWriter(output_excel) as writer:
    df_user.to_excel(writer, sheet_name="Concentrado", index=False, header=False)
print("Done!")
