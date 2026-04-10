"""
ACTUALIZADOR AUTOMÃTICO â€” TABLERO SARAMPIÃ“N DURANGO
====================================================
Corre automÃ¡ticamente cada 3 dÃ­as con el Programador de tareas de Windows.

Requiere en la misma carpeta:
    - Poblacion_municipio_edad_simple_y_sexo_Mexico_2026_CENJSIA_EGM.xlsx
    - Vacunacion_SRP_SR_Cubos_Enero-Mayo_2025.xlsx
    - SRP-SR-*.csv  (el mÃ¡s reciente se usa automÃ¡ticamente)

Genera:
    - index.html  (tablero web listo para GitHub Pages)

Y lo sube automÃ¡ticamente a GitHub si tienes Git configurado.
"""

import pandas as pd
import numpy as np
import os, json, unicodedata, re, sys, subprocess
from io import StringIO
from datetime import datetime, date
import locale

# â”€â”€â”€ CONFIGURACIÃ“N â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Repositorio GitHub (cambia si es diferente)
GITHUB_REPO_URL = "https://github.com/aliciaesparza-sol/tablero-sarampion-v2.git"
GITHUB_BRANCH   = "master"

# Archivo de salida
OUTPUT_HTML = os.path.join(BASE_DIR, "index.html")

# â”€â”€â”€ MUNICIPIOS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
MUNICIPIOS_39 = [
    "CanatlÃ¡n","Canelas","Coneto de Comonfort","CuencamÃ©","Durango","El Oro",
    "General SimÃ³n BolÃ­var","GÃ³mez Palacio","Guadalupe Victoria","GuanacevÃ­",
    "Hidalgo","IndÃ©","Lerdo","MapimÃ­","Mezquital","Nazas","Nombre de Dios",
    "Nuevo Ideal","Ocampo","OtÃ¡ez","PÃ¡nuco de Coronado","PeÃ±Ã³n Blanco",
    "Poanas","Pueblo Nuevo","Rodeo","San Bernardo","San Dimas",
    "San Juan de Guadalupe","San Juan del RÃ­o","San Luis del Cordero",
    "San Pedro del Gallo","Santa Clara","Santiago Papasquiaro","SÃºchil",
    "Tamazula","Tepehuanes","Tlahualilo","Topia","Vicente Guerrero"
]

GRUPOS_INFO = {
    "6-11m":  {"label": "6-11 Meses",        "emoji": "ðŸ¼", "meta_pct": 0.50, "edades": [0],              "tab": "g611"},
    "1anio":  {"label": "1 AÃ±o",              "emoji": "ðŸ‘¶", "meta_pct": 1.00, "edades": [1],              "tab": "g1a"},
    "18m":    {"label": "18 Meses",           "emoji": "ðŸ§’", "meta_pct": 1.00, "edades": [1],              "tab": "g18m"},
    "2-12":   {"label": "Rezag 2-12 AÃ±os",    "emoji": "ðŸ“š", "meta_pct": 0.50, "edades": list(range(2,13)),"tab": "g212"},
    "13-19":  {"label": "13-19 AÃ±os",         "emoji": "ðŸŽ“", "meta_pct": 0.50, "edades": list(range(13,20)),"tab": "g1319"},
    "20-39":  {"label": "20-39 AÃ±os",         "emoji": "ðŸ§‘", "meta_pct": 0.50, "edades": list(range(20,40)),"tab": "g2039"},
    "40-49":  {"label": "40-49 AÃ±os",         "emoji": "ðŸ‘©", "meta_pct": 0.50, "edades": list(range(40,50)),"tab": "g4049"},
}
GRUPOS_ORDER = ["6-11m","1anio","18m","2-12","13-19","20-39","40-49"]

def normalizar(s):
    if not isinstance(s, str): return ""
    s = s.strip().upper()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s)

NORM_MAP = {normalizar(m): m for m in MUNICIPIOS_39}

def match_mun(raw):
    if not isinstance(raw, str): return None
    raw = raw.replace("Ãƒ\x91","Ã‘").replace("ÃƒÂ±","Ã±").replace("ORO EL","EL ORO")
    n = normalizar(raw)
    if n in NORM_MAP: return NORM_MAP[n]
    for k, v in NORM_MAP.items():
        if n in k or k in n: return v
    return None

def semaforo(cob):
    if cob >= 95:  return "âœ… META ALCANZADA"
    if cob >= 80:  return "ðŸŸ¢ EN PROCESO AVANZADO"
    if cob >= 50:  return "ðŸŸ¡ EN PROCESO"
    if cob >= 25:  return "ðŸŸ  REZAGO MODERADO"
    return "ðŸ”´ CRÃTICO"

def col_num(df, col):
    if col not in df.columns: return pd.Series(0, index=df.index)
    return pd.to_numeric(df[col], errors="coerce").fillna(0)


# â”€â”€â”€ PASO 1: LEER POBLACIÃ“N CONAPO â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("ðŸ“– Leyendo poblaciÃ³n CONAPO 2026...")
FILE_POB = os.path.join(BASE_DIR, "Poblacion_municipio_edad_simple_y_sexo_Mexico_2026_CENJSIA_EGM.xlsx")
if not os.path.exists(FILE_POB):
    print(f"âŒ No se encontrÃ³: {FILE_POB}")
    sys.exit(1)

raw_pob = pd.read_excel(FILE_POB, sheet_name="Durango", header=None)
headers_pob = raw_pob.iloc[4].tolist()

row_h_start = 6
row_m_start = None
for i in range(100, 140):
    if str(raw_pob.iloc[i, 0]).strip() == "Mujeres":
        row_m_start = i + 1
        break
if row_m_start is None:
    row_m_start = 124

pob_dict = {}
for ci, mun_name in enumerate(headers_pob):
    if not isinstance(mun_name, str): continue
    if mun_name in ("Edad", "Poblacion Total H y M"): continue
    matched = match_mun(mun_name)
    if matched is None: continue
    edades_h, edades_m = {}, {}
    for row_i in range(row_h_start, row_h_start + 86):
        edad = raw_pob.iloc[row_i, 0]
        try: edad = int(edad)
        except: break
        val = raw_pob.iloc[row_i, ci]
        edades_h[edad] = int(val) if pd.notna(val) else 0
    for row_i in range(row_m_start, row_m_start + 86):
        edad = raw_pob.iloc[row_i, 0]
        try: edad = int(edad)
        except: break
        val = raw_pob.iloc[row_i, ci]
        edades_m[edad] = int(val) if pd.notna(val) else 0
    edades_tot = {e: edades_h.get(e,0) + edades_m.get(e,0) for e in range(86)}
    if matched not in pob_dict:
        pob_dict[matched] = edades_tot
    else:
        for e in range(86):
            pob_dict[matched][e] = pob_dict[matched].get(e,0) + edades_tot.get(e,0)

print(f"   âœ“ {len(pob_dict)} municipios cargados")

def pob_mun(mun, edades):
    d = pob_dict.get(mun, {})
    return sum(d.get(e,0) for e in edades)

def universo_grupo(mun, grupo):
    info = GRUPOS_INFO[grupo]
    edades = info["edades"]
    if grupo == "6-11m":
        return int(round(pob_mun(mun, edades) * 0.5))
    return pob_mun(mun, edades)


# â”€â”€â”€ PASO 2: LEER CUBOS ENE-MAY 2025 â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("ðŸ“– Leyendo cubos Ene-May 2025...")
FILE_CUBOS = os.path.join(BASE_DIR, "Vacunacion_SRP_SR_Cubos_Enero-Mayo_2025.xlsx")

cubos_por_grupo_estatal = {g: 0 for g in GRUPOS_ORDER}

if os.path.exists(FILE_CUBOS):
    try:
        df_cubos = pd.read_excel(FILE_CUBOS, sheet_name="Sheet1", engine="openpyxl")
        df_cubos.columns = df_cubos.columns.str.strip()

        def c_cubos(col):
            if col not in df_cubos.columns: return 0
            return pd.to_numeric(df_cubos[col], errors="coerce").fillna(0).sum()

        cubos_por_grupo_estatal["1anio"] = c_cubos("VAC23 PRIMERA 12 MESES (Total)")
        cubos_por_grupo_estatal["18m"]   = c_cubos("VTV01 SEGUNDA 18 MESES (Total)")
        c212 = (c_cubos("VAC81 SEGUNDA 6 AÃ‘OS (Total)") +
                c_cubos("VTV02 INICIAR/COMPLETAR 1RA 13M-9A (Total)") +
                c_cubos("VTV03 INICIAR/COMPLETAR 2DA 19M-9A (Total)"))
        cubos_por_grupo_estatal["2-12"] = c212
        sr_total = c_cubos("Total SR DOBLE VIRAL (Total)")
        cubos_por_grupo_estatal["20-39"] = sr_total * 0.5
        cubos_por_grupo_estatal["40-49"] = sr_total * 0.5
        print(f"   âœ“ Cubos cargados correctamente")
    except Exception as e:
        print(f"   âš ï¸  Error leyendo cubos: {e} â€” se usarÃ¡ 0")
else:
    print("   âš ï¸  Archivo de cubos no encontrado â€” se usarÃ¡ 0")


# â”€â”€â”€ PASO 3: LEER CSV NOMINAL â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
import glob
csv_candidates = sorted(glob.glob(os.path.join(BASE_DIR, "SRP-SR-*.csv")))
if not csv_candidates:
    print("âŒ No se encontrÃ³ ningÃºn CSV SRP-SR-*.csv")
    sys.exit(1)

FILE_CSV = max(csv_candidates, key=os.path.getmtime)
print(f"ðŸ“– Leyendo CSV nominal: {os.path.basename(FILE_CSV)}...")

with open(FILE_CSV, encoding="latin1") as f:
    content = f.read()

lines = content.split("\n")
fixed = []
for line in lines:
    if line.startswith('"') and line.endswith('"'):
        line = line[1:-1].replace('""', '"')
    fixed.append(line)

df_nom = pd.read_csv(StringIO("\n".join(fixed)), encoding="latin1", low_memory=False)
df_nom.columns = df_nom.columns.str.strip()

if "ESTADO" in df_nom.columns:
    df_nom = df_nom[df_nom["ESTADO"].str.strip() == "DURANGO"].copy()

df_nom["MUN_MATCH"] = df_nom["MUNICIPIO"].apply(match_mun)
df_nom = df_nom[df_nom["MUN_MATCH"].notna()].copy()

fecha_max = None
if "Fecha de registro" in df_nom.columns:
    df_nom["Fecha de registro"] = pd.to_datetime(df_nom["Fecha de registro"], errors="coerce")
    fecha_max = df_nom["Fecha de registro"].max()

print(f"   âœ“ {len(df_nom)} registros de Durango")

def dosis_grupo_nom(grupo):
    if grupo == "6-11m":
        v = col_num(df_nom,"SRP 6 A 11 MESES PRIMERA") + col_num(df_nom,"SR 6 A 11 MESES PRIMERA")
    elif grupo == "1anio":
        v = col_num(df_nom,"SRP 1 ANIO  PRIMERA") + col_num(df_nom,"SR 1 ANIO PRIMERA")
    elif grupo == "18m":
        v = col_num(df_nom,"SRP 18 MESES SEGUNDA") + col_num(df_nom,"SR 18 MESES SEGUNDA")
    elif grupo == "2-12":
        v = sum(col_num(df_nom, c) for c in [
            "SRP 2 A 5 ANIOS PRIMERA","SRP 6 ANIOS PRIMERA","SRP 7 A 9 ANIOS PRIMERA","SRP 10 A 12 ANIOS PRIMERA",
            "SRP 2 A 5 ANIOS SEGUNDA","SRP 6 ANIOS SEGUNDA","SRP 7 A 9 ANIOS SEGUNDA","SRP 10 A 12 ANIOS SEGUNDA",
            "SR 2 A 5 ANIOS PRIMERA","SR 6 ANIOS PRIMERA","SR 7 A 9 ANIOS PRIMERA","SR 10 A 12 ANIOS PRIMERA",
            "SR 2 A 5 ANIOS SEGUNDA","SR 6 ANIOS SEGUNDA","SR 7 A 9 ANIOS SEGUNDA","SR 10 A 12 ANIOS SEGUNDA"])
    elif grupo == "13-19":
        v = sum(col_num(df_nom, c) for c in [
            "SRP 13 A 19 ANIOS PRIMERA","SRP 13 A 19 ANIOS SEGUNDA",
            "SR 13 A 19 ANIOS PRIMERA","SR 13 A 19 ANIOS SEGUNDA"])
    elif grupo == "20-39":
        v = sum(col_num(df_nom, c) for c in [
            "SRP 20 A 29 ANIOS PRIMERA","SRP 20 A 29 ANIOS SEGUNDA","SRP 30 A 39 ANIOS PRIMERA","SRP 30 A 39 ANIOS SEGUNDA",
            "SR 20 A 29 ANIOS PRIMERA","SR 20 A 29 ANIOS SEGUNDA","SR 30 A 39 ANIOS PRIMERA","SR 30 A 39 ANIOS SEGUNDA"])
    elif grupo == "40-49":
        v = sum(col_num(df_nom, c) for c in [
            "SRP 40 A 49 ANIOS PRIMERA","SRP 40 A 49 ANIOS SEGUNDA",
            "SR 40 A 49 ANIOS PRIMERA","SR 40 A 49 ANIOS SEGUNDA"])
    else:
        v = pd.Series(0, index=df_nom.index)
    df_nom["_v"] = v
    return df_nom.groupby("MUN_MATCH")["_v"].sum()


# â”€â”€â”€ PASO 4: CALCULAR COBERTURAS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("âš™ï¸  Calculando coberturas...")

tablas = {}
for grupo in GRUPOS_ORDER:
    info = GRUPOS_INFO[grupo]
    meta_pct = info["meta_pct"]
    cubos_est = cubos_por_grupo_estatal[grupo]
    univ_est = sum(universo_grupo(m, grupo) for m in MUNICIPIOS_39)
    nom_series = dosis_grupo_nom(grupo)

    rows = []
    for mun in MUNICIPIOS_39:
        univ = universo_grupo(mun, grupo)
        meta = int(round(univ * meta_pct))
        cubos_m = int(round(cubos_est * (univ / univ_est))) if univ_est > 0 else 0
        nominal = int(nom_series.get(mun, 0))
        total = cubos_m + nominal
        pendientes = max(0, meta - total)
        cob = round(total / meta * 100, 1) if meta > 0 else 0.0
        rows.append({
            "municipio": mun, "universo": univ, "meta": meta,
            "cubos": cubos_m, "nominal": nominal, "total": total,
            "pendientes": pendientes, "cobertura": cob,
            "semaforo": semaforo(cob)
        })

    df_g = pd.DataFrame(rows).sort_values("cobertura").reset_index(drop=True)
    tablas[grupo] = df_g
    print(f"   âœ“ {info['emoji']} {info['label']}")

# Resumen total
resumen_rows = []
for mun in MUNICIPIOS_39:
    univ_t = sum(universo_grupo(mun, g) for g in GRUPOS_ORDER)
    meta_t  = sum(int(tablas[g][tablas[g]["municipio"]==mun]["meta"].values[0]) for g in GRUPOS_ORDER)
    cubos_t = sum(int(tablas[g][tablas[g]["municipio"]==mun]["cubos"].values[0]) for g in GRUPOS_ORDER)
    nom_t   = sum(int(tablas[g][tablas[g]["municipio"]==mun]["nominal"].values[0]) for g in GRUPOS_ORDER)
    total_t = cubos_t + nom_t
    pend_t  = max(0, meta_t - total_t)
    cob_t   = round(total_t / meta_t * 100, 1) if meta_t > 0 else 0.0
    resumen_rows.append({
        "municipio": mun, "universo": univ_t, "meta": meta_t,
        "cubos": cubos_t, "nominal": nom_t, "total": total_t,
        "pendientes": pend_t, "cobertura": cob_t, "semaforo": semaforo(cob_t)
    })

df_resumen = pd.DataFrame(resumen_rows).sort_values("cobertura").reset_index(drop=True)

# Totales generales
r = df_resumen
univ_tot  = int(r["universo"].sum())
meta_tot  = int(r["meta"].sum())
cubos_tot = int(r["cubos"].sum())
nom_tot   = int(r["nominal"].sum())
total_tot = int(r["total"].sum())
cob_tot   = round(total_tot / meta_tot * 100, 1) if meta_tot > 0 else 0.0

try: locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
except:
    try: locale.setlocale(locale.LC_TIME, 'Spanish_Mexico.1252')
    except: pass

fecha_corte = fecha_max.strftime("%d de %B de %Y") if fecha_max and pd.notna(fecha_max) else date.today().strftime("%d/%m/%Y")
semana_num  = datetime.now().isocalendar()[1]

print(f"   âœ“ Total dosis: {total_tot:,} | Cobertura: {cob_tot}%")


# â”€â”€â”€ PASO 5: CONSTRUIR JSON para el HTML â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def build_group_json(grupo):
    df_g = tablas[grupo]
    info = GRUPOS_INFO[grupo]
    rows_data = df_g.to_dict(orient="records")
    # Agregar TOTAL DURANGO
    univ_g  = int(df_g["universo"].sum())
    meta_g  = int(df_g["meta"].sum())
    cubos_g = int(df_g["cubos"].sum())
    nom_g   = int(df_g["nominal"].sum())
    tot_g   = int(df_g["total"].sum())
    pend_g  = max(0, meta_g - tot_g)
    cob_g   = round(tot_g / meta_g * 100, 1) if meta_g > 0 else 0.0
    rows_data.append({
        "municipio": "TOTAL DURANGO", "universo": univ_g, "meta": meta_g,
        "cubos": cubos_g, "nominal": nom_g, "total": tot_g,
        "pendientes": pend_g, "cobertura": cob_g, "semaforo": semaforo(cob_g)
    })
    return {
        "label": f"{info['emoji']} {info['label']}",
        "pct_meta": int(info["meta_pct"] * 100),
        "resumen": {"universo": univ_g, "meta": meta_g, "cubos": cubos_g,
                    "nominal": nom_g, "total": tot_g, "cobertura": cob_g},
        "municipios": rows_data
    }

DATA = {}
for grupo in GRUPOS_ORDER:
    tab_key = GRUPOS_INFO[grupo]["tab"]
    DATA[tab_key] = build_group_json(grupo)

resumen_rows_data = df_resumen.to_dict(orient="records")
resumen_rows_data.append({
    "municipio": "TOTAL DURANGO", "universo": univ_tot, "meta": meta_tot,
    "cubos": cubos_tot, "nominal": nom_tot, "total": total_tot,
    "pendientes": max(0, meta_tot - total_tot), "cobertura": cob_tot,
    "semaforo": semaforo(cob_tot)
})
DATA["resumen"] = {
    "resumen": {"universo": univ_tot, "meta": meta_tot, "cubos": cubos_tot,
                "nominal": nom_tot, "total": total_tot, "cobertura": cob_tot},
    "municipios": resumen_rows_data
}

data_json = json.dumps(DATA, ensure_ascii=False)


# â”€â”€â”€ PASO 6: GENERAR HTML â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("ðŸŒ Generando HTML del tablero...")

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tablero Cobertura SarampiÃ³n â€” Durango</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
  :root {{
    --bg:#f0f2f5;--card:#fff;--border:#e2e6ea;--text:#1a2332;--sub:#5a6a7a;
    --accent:#1a6fc4;--meta:#16a34a;--critico:#dc2626;--proceso:#ca8a04;
    --header-bg:#1a2332;
  }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);font-size:13px}}
  .header{{background:var(--header-bg);color:#fff;padding:14px 24px;display:flex;align-items:center;
    justify-content:space-between;position:sticky;top:0;z-index:100;box-shadow:0 2px 8px rgba(0,0,0,.25)}}
  .header-left{{display:flex;align-items:center;gap:14px}}
  .logo{{width:46px;height:46px;background:#2563eb;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:22px}}
  .header-title h1{{font-size:17px;font-weight:700}}
  .header-title p{{font-size:11px;color:#94a3b8;margin-top:2px}}
  .header-badge{{background:#16a34a;color:#fff;padding:8px 16px;border-radius:10px;text-align:center;font-weight:700}}
  .header-badge .pct{{font-size:22px;line-height:1}}
  .header-badge .lbl{{font-size:10px;opacity:.9;margin-top:2px}}
  .semaforo-bar{{background:#fff;border-bottom:1px solid var(--border);padding:8px 24px;display:flex;align-items:center;gap:6px;flex-wrap:wrap}}
  .semaforo-bar span{{font-size:11px;color:var(--sub);margin-right:4px}}
  .sem-pill{{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:600}}
  .sem-meta{{background:#dcfce7;color:#15803d}}.sem-avanzado{{background:#d1fae5;color:#065f46}}
  .sem-proceso{{background:#fef9c3;color:#a16207}}.sem-rezago{{background:#ffedd5;color:#c2410c}}
  .sem-critico{{background:#fee2e2;color:#b91c1c}}
  .tabs-wrap{{background:#fff;border-bottom:1px solid var(--border);padding:0 24px}}
  .tabs{{display:flex;gap:2px;overflow-x:auto}}
  .tab{{padding:11px 16px;cursor:pointer;font-size:12px;font-weight:600;border-bottom:3px solid transparent;
    white-space:nowrap;color:var(--sub);transition:all .15s}}
  .tab:hover{{color:var(--text)}}.tab.active{{color:var(--accent);border-bottom-color:var(--accent)}}
  .content{{padding:20px 24px}}
  .kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:18px}}
  .kpi{{background:#fff;border-radius:10px;padding:14px 16px;border:1px solid var(--border);border-top:3px solid var(--accent)}}
  .kpi.meta-card{{border-top-color:var(--meta)}}.kpi.pend-card{{border-top-color:var(--critico)}}.kpi.cob-card{{border-top-color:var(--proceso)}}
  .kpi label{{font-size:10px;text-transform:uppercase;letter-spacing:.6px;color:var(--sub);font-weight:600}}
  .kpi .val{{font-size:22px;font-weight:700;margin-top:4px;font-family:'DM Mono',monospace}}
  .kpi .val.meta-v{{color:var(--meta)}}.kpi .val.pend-v{{color:var(--critico)}}.kpi .val.cob-v{{color:var(--proceso)}}
  .group-info{{background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;padding:10px 16px;
    margin-bottom:14px;font-size:12px;color:#1e40af;display:flex;gap:20px;flex-wrap:wrap}}
  .table-wrap{{background:#fff;border-radius:12px;border:1px solid var(--border);overflow:hidden}}
  .table-header{{padding:12px 16px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border)}}
  .table-header h3{{font-size:13px;font-weight:700}}
  .search-input{{padding:6px 12px;border:1px solid var(--border);border-radius:6px;font-size:12px;
    font-family:inherit;outline:none;width:200px}}
  .search-input:focus{{border-color:var(--accent)}}
  table{{width:100%;border-collapse:collapse}}
  thead th{{background:#f8fafc;padding:9px 12px;text-align:left;font-size:11px;font-weight:700;
    text-transform:uppercase;letter-spacing:.5px;color:var(--sub);border-bottom:1px solid var(--border);white-space:nowrap}}
  thead th.num{{text-align:right}}
  tbody tr{{transition:background .1s}}
  tbody tr:hover{{background:#f8fafc}}
  tbody tr.total-row{{background:#f1f5f9;font-weight:700;border-top:2px solid var(--border)}}
  tbody td{{padding:8px 12px;border-bottom:1px solid #f1f5f9;font-size:12px}}
  tbody td.num{{text-align:right;font-family:'DM Mono',monospace;font-size:11px}}
  tbody td.mun{{font-weight:600}}
  .badge{{display:inline-flex;align-items:center;gap:5px;padding:3px 8px;border-radius:20px;font-size:10px;font-weight:700;white-space:nowrap}}
  .badge .dot{{width:7px;height:7px;border-radius:50%}}
  .b-meta{{background:#dcfce7;color:#15803d}}.b-meta .dot{{background:#16a34a}}
  .b-avanzado{{background:#d1fae5;color:#065f46}}.b-avanzado .dot{{background:#059669}}
  .b-proceso{{background:#fef9c3;color:#92400e}}.b-proceso .dot{{background:#d97706}}
  .b-rezago{{background:#ffedd5;color:#9a3412}}.b-rezago .dot{{background:#ea580c}}
  .b-critico{{background:#fee2e2;color:#991b1b}}.b-critico .dot{{background:#dc2626}}
  .cob-cell{{display:flex;align-items:center;gap:8px}}
  .cob-bar-wrap{{width:60px;background:#e2e8f0;border-radius:4px;height:6px;flex-shrink:0;overflow:hidden}}
  .cob-bar{{height:100%;border-radius:4px}}
  .cob-val{{font-family:'DM Mono',monospace;font-size:11px;font-weight:600;min-width:38px}}
  .note{{font-size:10px;color:var(--sub);padding:10px 16px;font-style:italic}}
  .update-info{{font-size:11px;color:#94a3b8;text-align:right;padding:8px 24px;background:#fff;border-top:1px solid var(--border)}}
</style>
</head>
<body>
<div class="header">
  <div class="header-left">
    <div class="logo">ðŸ¦ </div>
    <div class="header-title">
      <h1>Cobertura SarampiÃ³n SRP/SR</h1>
      <p>SERVICIOS DE SALUD DE DURANGO &nbsp;Â·&nbsp; CONAPO 2026 &nbsp;Â·&nbsp; Corte: {fecha_corte} &nbsp;Â·&nbsp; Semana {semana_num}</p>
    </div>
  </div>
  <div class="header-badge">
    <div class="pct">{cob_tot}%</div>
    <div class="lbl">{semaforo(cob_tot)}</div>
  </div>
</div>
<div class="semaforo-bar">
  <span>SemÃ¡foro:</span>
  <div class="sem-pill sem-meta">âœ… â‰¥95% META</div>
  <div class="sem-pill sem-avanzado">ðŸŸ¢ 80-94%</div>
  <div class="sem-pill sem-proceso">ðŸŸ¡ 50-79%</div>
  <div class="sem-pill sem-rezago">ðŸŸ  25-49%</div>
  <div class="sem-pill sem-critico">ðŸ”´ &lt;25%</div>
</div>
<div class="tabs-wrap">
  <div class="tabs" id="tabs">
    <div class="tab active" data-tab="resumen">ðŸ“Š Resumen Total</div>
    <div class="tab" data-tab="g611">ðŸ¼ 6-11 Meses</div>
    <div class="tab" data-tab="g1a">ðŸ‘¶ 1 AÃ±o</div>
    <div class="tab" data-tab="g18m">ðŸ§’ 18 Meses</div>
    <div class="tab" data-tab="g212">ðŸ“š Rezag 2-12 AÃ±os</div>
    <div class="tab" data-tab="g1319">ðŸŽ“ 13-19 AÃ±os</div>
    <div class="tab" data-tab="g2039">ðŸ§‘ 20-39 AÃ±os</div>
    <div class="tab" data-tab="g4049">ðŸ‘© 40-49 AÃ±os</div>
  </div>
</div>
<div class="content" id="content"></div>
<div class="update-info">Ãšltima actualizaciÃ³n: {datetime.now().strftime('%d/%m/%Y %H:%M')} hrs</div>

<script>
const DATA = {data_json};
function fmt(n){{return n===undefined||n===null?'â€”':n.toLocaleString('es-MX')}}
function fmtPct(n){{return n===undefined||n===null?'â€”':n.toFixed(1)+'%'}}
function semClass(sem){{
  if(!sem)return'';
  if(sem.includes('META'))return'b-meta';
  if(sem.includes('AVANZADO'))return'b-avanzado';
  if(sem.includes('PROCESO'))return'b-proceso';
  if(sem.includes('REZAGO'))return'b-rezago';
  if(sem.includes('CRÃTICO'))return'b-critico';
  return'';
}}
function semLabel(sem){{
  if(!sem)return'';
  if(sem.includes('META'))return'âœ… META';
  if(sem.includes('AVANZADO'))return'ðŸŸ¢ AVANZADO';
  if(sem.includes('PROCESO'))return'ðŸŸ¡ EN PROCESO';
  if(sem.includes('REZAGO'))return'ðŸŸ  REZAGO';
  if(sem.includes('CRÃTICO'))return'ðŸ”´ CRÃTICO';
  return sem;
}}
function cobColor(c){{
  if(c>=95)return'#16a34a';if(c>=80)return'#15803d';
  if(c>=50)return'#ca8a04';if(c>=25)return'#ea580c';return'#dc2626';
}}
function cobBarWidth(c){{return Math.min(c,100)}}
function tableRows(rows, hasCubos){{
  return rows.filter(m=>m.municipio&&!m.municipio.startsWith('*')).map(m=>{{
    const isTotal=m.municipio==='TOTAL DURANGO';
    return `<tr class="${{isTotal?'total-row':''}}">
      <td class="mun">${{m.municipio}}</td>
      <td class="num">${{fmt(m.universo)}}</td>
      <td class="num">${{fmt(m.meta)}}</td>
      ${{hasCubos?`<td class="num">${{fmt(m.cubos)}}</td>`:''}}
      <td class="num">${{fmt(m.nominal)}}</td>
      <td class="num">${{fmt(m.total)}}</td>
      <td class="num" style="color:${{m.pendientes>0?'#dc2626':'#16a34a'}}">${{fmt(m.pendientes)}}</td>
      <td class="num">
        <div class="cob-cell">
          <div class="cob-bar-wrap"><div class="cob-bar" style="width:${{cobBarWidth(m.cobertura)}}%;background:${{cobColor(m.cobertura)}}"></div></div>
          <span class="cob-val" style="color:${{cobColor(m.cobertura)}}">${{fmtPct(m.cobertura)}}</span>
        </div>
      </td>
      <td><span class="badge ${{semClass(m.semaforo)}}"><span class="dot"></span>${{semLabel(m.semaforo)}}</span></td>
    </tr>`;
  }}).join('');
}}
function renderResumen(){{
  const d=DATA.resumen,r=d.resumen;
  return `
    <div class="kpis">
      <div class="kpi"><label>Universo CONAPO 2026</label><div class="val">${{fmt(r.universo)}}</div></div>
      <div class="kpi meta-card"><label>Meta Sectorial</label><div class="val meta-v">${{fmt(r.meta)}}</div></div>
      <div class="kpi"><label>Cubos Ene-May 25</label><div class="val">${{fmt(r.cubos)}}</div></div>
      <div class="kpi"><label>Nominal</label><div class="val">${{fmt(r.nominal)}}</div></div>
      <div class="kpi"><label>Total Dosis</label><div class="val">${{fmt(r.total)}}</div></div>
      <div class="kpi pend-card"><label>Pendientes</label><div class="val pend-v">${{fmt(Math.max(0,r.meta-r.total))}}</div></div>
      <div class="kpi cob-card"><label>% Cobertura</label><div class="val cob-v">${{fmtPct(r.cobertura)}}</div></div>
    </div>
    <div class="table-wrap">
      <div class="table-header"><h3>ðŸ“Š Todos los Municipios â€” Todos los Grupos</h3>
        <input class="search-input" id="search-resumen" placeholder="ðŸ” Buscar municipio..." oninput="filterTable('resumen')">
      </div>
      <table id="tbl-resumen"><thead><tr>
        <th>Municipio</th><th class="num">Universo</th><th class="num">Meta</th>
        <th class="num">Cubos</th><th class="num">Nominal</th><th class="num">Total</th>
        <th class="num">Pendientes</th><th class="num">% Cob</th><th>SemÃ¡foro</th>
      </tr></thead><tbody>${{tableRows(d.municipios,true)}}</tbody></table>
      <div class="note">* Cubos ene-may 2025 distribuidos proporcionalmente por municipio segÃºn universo CONAPO 2026.</div>
    </div>`;
}}
function renderGroup(key){{
  const d=DATA[key],r=d.resumen;
  const hasCubos=d.municipios.some(m=>m.cubos>0);
  return `
    <div class="group-info">
      <span><strong>${{d.label}}</strong></span>
      <span>% Meta: <strong>${{d.pct_meta}}%</strong></span>
      <span>Universo: <strong>${{fmt(r.universo)}}</strong></span>
      <span>Meta: <strong>${{fmt(r.meta)}}</strong></span>
      <span>Cobertura: <strong style="color:${{cobColor(r.cobertura)}}">${{fmtPct(r.cobertura)}}</strong></span>
    </div>
    <div class="kpis">
      <div class="kpi"><label>Universo</label><div class="val">${{fmt(r.universo)}}</div></div>
      <div class="kpi meta-card"><label>Meta (${{d.pct_meta}}%)</label><div class="val meta-v">${{fmt(r.meta)}}</div></div>
      ${{hasCubos?`<div class="kpi"><label>Cubos</label><div class="val">${{fmt(r.cubos)}}</div></div>`:''}}
      <div class="kpi"><label>Nominal</label><div class="val">${{fmt(r.nominal)}}</div></div>
      <div class="kpi"><label>Total Dosis</label><div class="val">${{fmt(r.total)}}</div></div>
      <div class="kpi pend-card"><label>Pendientes</label><div class="val pend-v">${{fmt(Math.max(0,r.meta-r.total))}}</div></div>
      <div class="kpi cob-card"><label>% Cobertura</label><div class="val cob-v">${{fmtPct(r.cobertura)}}</div></div>
    </div>
    <div class="table-wrap">
      <div class="table-header"><h3>${{d.label}} â€” Cobertura por Municipio</h3>
        <input class="search-input" id="search-${{key}}" placeholder="ðŸ” Buscar municipio..." oninput="filterTable('${{key}}')">
      </div>
      <table id="tbl-${{key}}"><thead><tr>
        <th>Municipio</th><th class="num">Universo</th><th class="num">Meta</th>
        ${{hasCubos?'<th class="num">Cubos</th>':''}}
        <th class="num">Nominal</th><th class="num">Total</th>
        <th class="num">Pendientes</th><th class="num">% Cob</th><th>SemÃ¡foro</th>
      </tr></thead><tbody>${{tableRows(d.municipios,hasCubos)}}</tbody></table>
      <div class="note">* Cubos ene-may 2025 distribuidos proporcionalmente por municipio segÃºn universo CONAPO 2026.</div>
    </div>`;
}}
function filterTable(key){{
  const q=document.getElementById(`search-${{key}}`).value.toLowerCase();
  document.querySelectorAll(`#tbl-${{key}} tbody tr`).forEach(r=>{{
    r.style.display=r.cells[0].textContent.toLowerCase().includes(q)?'':'none';
  }});
}}
function renderTab(tab){{
  document.getElementById('content').innerHTML=tab==='resumen'?renderResumen():renderGroup(tab);
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.tab===tab));
}}
document.getElementById('tabs').addEventListener('click',e=>{{
  const t=e.target.closest('.tab');if(t)renderTab(t.dataset.tab);
}});
renderTab('resumen');
</script>
</body>
</html>"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"   âœ“ HTML generado: {OUTPUT_HTML}")


# â”€â”€â”€ PASO 7: SUBIR A GITHUB â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
print("ðŸš€ Subiendo a GitHub...")

def run_git(args, cwd):
    result = subprocess.run(
        ["git"] + args, cwd=cwd, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"   âš ï¸  git {' '.join(args)}: {result.stderr.strip()}")
    return result.returncode == 0

ok = True
ok = ok and run_git(["add", "index.html"], BASE_DIR)
ok = ok and run_git(["commit", "-m", f"ActualizaciÃ³n automÃ¡tica: {date.today()} â€” Cob {cob_tot}%"], BASE_DIR)
ok = ok and run_git(["push", "origin", "HEAD:master"], BASE_DIR)

if ok:
    print(f"   âœ“ Publicado en: https://aliciaesparza-sol.github.io/tablero-sarampion-v2/")
else:
    print("   âš ï¸  No se pudo subir a GitHub (revisa la conexiÃ³n o credenciales)")
    print(f"      El HTML sÃ­ se generÃ³ en: {OUTPUT_HTML}")

print(f"\nðŸŽ‰ Proceso completado â€” {datetime.now().strftime('%d/%m/%Y %H:%M')}")
print(f"   Cobertura total: {cob_tot}% | Total dosis: {total_tot:,}")

