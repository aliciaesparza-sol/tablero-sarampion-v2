"""
Actualizar el tablero de coberturas de sarampion con los datos mas recientes de CeNSIA.
Fuente: CSV descargado de CeNSIA (SRP-SR-2025_28-03-2026).
"""
import pandas as pd
import os, json, glob, unicodedata, re
from datetime import datetime

# === RUTAS ===
downloads = r"c:\Users\aicil\Downloads"
scratch   = r"C:\Users\aicil\.gemini\antigravity\scratch"

local_csv = os.path.join(scratch, "censia_latest.csv")
if os.path.exists(local_csv):
    csv_path = local_csv
else:
    # Buscar el CSV mas reciente de SRP en Downloads
    csv_files = sorted(glob.glob(os.path.join(downloads, "SRP-SR-2025_*.csv")), reverse=True)
    if not csv_files:
        raise FileNotFoundError("No se encontro ningun CSV local ni en Descargas.")
    csv_path = csv_files[0]
print(f"Usando CSV: {csv_path}")

# Leer CSV
df = pd.read_csv(csv_path, encoding="latin1", low_memory=False)
print(f"Columnas: {df.columns.tolist()}")
print(f"Filas: {len(df)}")

# Identificar columnas de dosis por grupo de edad
columnas = df.columns.tolist()
grupos = {
    "12M":   [c for c in columnas if "1 ANIO"  in c.upper() or "12 MES" in c.upper()],
    "18M":   [c for c in columnas if "18 MES"  in c.upper()],
    "6A":    [c for c in columnas if "6 ANI"   in c.upper()],
    "10_49": [c for c in columnas if any(k in c.upper() for k in ["10 A 12","13 A 19","20 A 39","40 A 49"])],
}

todas_cols_dosis = [c for g in grupos.values() for c in g]
df[todas_cols_dosis] = df[todas_cols_dosis].apply(pd.to_numeric, errors="coerce").fillna(0)
df["TOTAL_DOSIS"] = df[todas_cols_dosis].sum(axis=1)

# Municipios
if "MUNICIPIO" not in df.columns:
    # Buscar columna similar
    muni_col = [c for c in df.columns if "MUNIC" in c.upper()]
    if muni_col:
        df.rename(columns={muni_col[0]: "MUNICIPIO"}, inplace=True)
    else:
        raise ValueError("No se encontro columna MUNICIPIO en el CSV.")

# Cargar metas de poblacion desde el Excel de cobertura
excel_adult  = os.path.join(scratch, "COBERTURAS_UPDATED_2025.xlsx")
excel_infant = os.path.join(scratch, "coverage_infants_copy.xlsx")

def to_num(v):
    try: return float(pd.to_numeric(v, errors="coerce") or 0)
    except: return 0.0

def normalize(s):
    s = str(s).upper().strip()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', s)

# Leer metas municipales
meta_adult  = pd.read_excel(excel_adult,  sheet_name="SE20",   header=None)
meta_infant = pd.read_excel(excel_infant, sheet_name="SE 53",  header=None)

def leer_metas(df_meta, col_idx, start_row=7):
    r = {}
    for i in range(start_row, len(df_meta)):
        nombre = normalize(str(df_meta.iloc[i, 0]))
        if nombre and nombre not in ["NAN", "TOTAL"]:
            r[nombre] = to_num(df_meta.iloc[i, col_idx])
    return r

metas_adult = leer_metas(meta_adult,  1)
metas_12m   = leer_metas(meta_infant, 1)
metas_18m   = leer_metas(meta_infant, 4)
metas_6a    = leer_metas(meta_infant, 7)

# --- Agregar dosis por municipio ---
agg = {}
for grupo, cols in grupos.items():
    agg[f"DOSIS_{grupo}"] = df.groupby("MUNICIPIO")[cols].sum().sum(axis=1)

df_muni = pd.DataFrame(agg)
df_muni["TOTAL"] = df_muni.sum(axis=1)
df_muni = df_muni.reset_index()

# --- Calcular coberturas ---
def calcular_coberturas(row):
    m_norm = normalize(row["MUNICIPIO"])
    meta_12 = metas_12m.get(m_norm, 0)
    meta_18 = metas_18m.get(m_norm, 0)
    meta_6a = metas_6a.get(m_norm, 0)
    meta_ad = metas_adult.get(m_norm, 0)
    meta_total = meta_12 + meta_18 + meta_6a + meta_ad

    cob_12  = (row["DOSIS_12M"]   / meta_12  * 100) if meta_12  > 0 else 0
    cob_18  = (row["DOSIS_18M"]   / meta_18  * 100) if meta_18  > 0 else 0
    cob_6a  = (row["DOSIS_6A"]    / meta_6a  * 100) if meta_6a  > 0 else 0
    cob_ad  = (row["DOSIS_10_49"] / meta_ad  * 100) if meta_ad  > 0 else 0
    cob_tot = (row["TOTAL"] / meta_total * 100) if meta_total > 0 else 0

    def sem(c):
        return "🔴" if c < 60 else ("🟡" if c < 85 else "🟢")

    return pd.Series({
        "META_TOTAL": meta_total,
        "COB_12M":   round(cob_12, 1),
        "COB_18M":   round(cob_18, 1),
        "COB_6A":    round(cob_6a, 1),
        "COB_ADULT": round(cob_ad, 1),
        "COBERTURA": round(cob_tot, 1),
        "SEMAFORO":  sem(cob_tot),
    })

df_cob = df_muni.join(df_muni.apply(calcular_coberturas, axis=1))

# --- Guardar resultados ---
out_json = os.path.join(scratch, "charts", "cobertura_municipal_latest.json")
os.makedirs(os.path.dirname(out_json), exist_ok=True)

records = df_cob.to_dict(orient="records")

from datetime import datetime
import locale
try: locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
except: pass
corte_str = datetime.now().strftime("%d de %B %Y").lower()

with open(out_json, "w", encoding="utf-8") as f:
    json.dump({
        "corte": corte_str,
        "semana": datetime.now().isocalendar()[1],
        "generado": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "municipios": records
    }, f, ensure_ascii=False, indent=2)

print(f"\n=== RESUMEN ===")
print(df_cob[["MUNICIPIO","TOTAL","COBERTURA","SEMAFORO"]].to_string(index=False))
print(f"\nJSON guardado en: {out_json}")
print(f"Total dosis procesadas: {int(df_cob['TOTAL'].sum()):,}")
