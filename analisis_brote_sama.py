import json
import csv
import shutil
import os
from datetime import datetime, timedelta
from collections import Counter

# --- Configuration ---
SRC_DIR = r"C:\Users\aicil\.gemini\antigravity-ide\scratch"
DEST_DIR = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\BROTE MAQUILA SAMA OOAD DGO"

# --- Load cases data ---
with open(os.path.join(SRC_DIR, "casos_tabla.json"), "r", encoding="utf-8") as f:
    cases = json.load(f)

print(f"Total de casos cargados: {len(cases)}")

# --- 1. Análisis descriptivo ---
n = len(cases)
edades = [c["edad"] for c in cases]
sexos = [c["sexo"] for c in cases]
instituciones = [c["institucion"] for c in cases]
colonias = [c["colonia"] for c in cases]
umfs = [c["umf"] for c in cases]

# Parse dates
def parse_date(d):
    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(d, fmt)
        except:
            continue
    return None

fechas_sintomas = [parse_date(c["fecha_sintomas"]) for c in cases]
fechas_atencion = [parse_date(c["fecha_atencion"]) for c in cases]

# Filter valid dates
fechas_sint_valid = [d for d in fechas_sintomas if d]
fecha_min = min(fechas_sint_valid)
fecha_max = max(fechas_sint_valid)

# --- Statistics ---
edad_prom = sum(edades) / n
edad_min = min(edades)
edad_max = max(edades)
edad_mediana = sorted(edades)[n // 2]

sexo_count = Counter(sexos)
inst_count = Counter(instituciones)
colonia_count = Counter(colonias)
umf_count = Counter(umfs)

# Tasa de ataque por grupo de edad
grupos_edad = {"18-24": (18, 24), "25-29": (25, 29), "30-34": (30, 34), "35-41": (35, 41)}
grupo_count = {}
for label, (lo, hi) in grupos_edad.items():
    grupo_count[label] = sum(1 for e in edades if lo <= e <= hi)

# Curva epidémica (por día de inicio de síntomas)
curva = Counter()
for d in fechas_sint_valid:
    curva[d.strftime("%Y-%m-%d")] += 1

# Sort by date
curva_sorted = sorted(curva.items())

# Intervalo entre síntomas y atención
intervalos = []
for fs, fa in zip(fechas_sintomas, fechas_atencion):
    if fs and fa:
        intervalos.append((fa - fs).days)
intervalo_prom = sum(intervalos) / len(intervalos) if intervalos else 0

# Dispersión geográfica
lats = [c["lat"] for c in cases]
lngs = [c["lng"] for c in cases]
lat_centro = sum(lats) / n
lng_centro = sum(lngs) / n

# Distancia máxima entre casos (aprox en km)
import math
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

max_dist = 0
for i in range(n):
    for j in range(i+1, n):
        d = haversine(lats[i], lngs[i], lats[j], lngs[j])
        if d > max_dist:
            max_dist = d

# --- 2. Build analysis report ---
report = f"""# ANÁLISIS EPIDEMIOLÓGICO - BROTE SARAMPIÓN MAQUILADORA SAMA
## OOAD Durango - Victoria de Durango, Durango
### Fecha de análisis: {datetime.now().strftime("%d/%m/%Y %H:%M")}

---

## 1. RESUMEN EJECUTIVO

Se analizan **{n} casos confirmados** de sarampión asociados al brote en la maquiladora SAMA, 
OOAD Durango. Los casos se presentaron en el periodo del **{fecha_min.strftime("%d/%m/%Y")}** al 
**{fecha_max.strftime("%d/%m/%Y")}** (inicio de síntomas), distribuidos en **{len(set(colonias))} colonias** 
del municipio de Victoria de Durango.

---

## 2. DISTRIBUCIÓN POR SEXO

| Sexo | Casos | Porcentaje |
|------|-------|------------|
| Femenino | {sexo_count.get("Femenino", 0)} | {sexo_count.get("Femenino", 0)/n*100:.1f}% |
| Masculino | {sexo_count.get("Masculino", 0)} | {sexo_count.get("Masculino", 0)/n*100:.1f}% |
| **Total** | **{n}** | **100%** |

**Razón M:F** = {sexo_count.get("Masculino", 0)/sexo_count.get("Femenino", 1):.2f}

---

## 3. DISTRIBUCIÓN POR GRUPO DE EDAD

| Grupo de edad | Casos | Porcentaje |
|---------------|-------|------------|
"""

for label, count in sorted(grupo_count.items()):
    report += f"| {label} años | {count} | {count/n*100:.1f}% |\n"

report += f"""| **Total** | **{n}** | **100%** |

- **Edad promedio**: {edad_prom:.1f} años
- **Edad mediana**: {edad_mediana} años
- **Rango de edad**: {edad_min} - {edad_max} años

---

## 4. DISTRIBUCIÓN POR INSTITUCIÓN NOTIFICANTE

| Institución | Casos | Porcentaje |
|-------------|-------|------------|
"""

for inst, count in inst_count.most_common():
    report += f"| {inst} | {count} | {count/n*100:.1f}% |\n"

report += f"""| **Total** | **{n}** | **100%** |

---

## 5. DISTRIBUCIÓN POR UMF NOTIFICANTE

| UMF | Casos | Porcentaje |
|-----|-------|------------|
"""

for umf, count in umf_count.most_common():
    report += f"| UMF {umf} | {count} | {count/n*100:.1f}% |\n"

report += f"""| **Total** | **{n}** | **100%** |

---

## 6. CURVA EPIDÉMICA (Inicio de Síntomas)

| Fecha | Casos | Acumulado |
|-------|-------|-----------|
"""

acum = 0
for fecha, count in curva_sorted:
    acum += count
    bar = "█" * count
    report += f"| {fecha} | {count} {bar} | {acum} |\n"

report += f"""
- **Periodo del brote**: {(fecha_max - fecha_min).days + 1} días
- **Pico**: {max(curva.values())} casos en un solo día

---

## 7. DISTRIBUCIÓN GEOGRÁFICA POR COLONIA

| Colonia | Casos | Porcentaje |
|---------|-------|------------|
"""

for col, count in colonia_count.most_common():
    report += f"| {col} | {count} | {count/n*100:.1f}% |\n"

report += f"""| **Total** | **{n}** | **100%** |

- **Colonias afectadas**: {len(set(colonias))}
- **Dispersión máxima**: {max_dist:.2f} km entre el caso más distante
- **Centro geográfico**: Lat {lat_centro:.4f}, Lng {lng_centro:.4f}

---

## 8. OPORTUNIDAD DE ATENCIÓN

| Indicador | Valor |
|-----------|-------|
| Intervalo promedio síntomas→atención | {intervalo_prom:.1f} días |
| Intervalo mínimo | {min(intervalos)} días |
| Intervalo máximo | {max(intervalos)} días |

### Detalle por caso:

| Caso | Síntomas | Atención | Intervalo (días) |
|------|----------|----------|-------------------|
"""

for c, fs, fa, intv in zip(cases, fechas_sintomas, fechas_atencion, intervalos):
    report += f"| {c['nombre']} | {fs.strftime('%d/%m/%Y') if fs else 'N/D'} | {fa.strftime('%d/%m/%Y') if fa else 'N/D'} | {intv} |\n"

report += f"""

---

## 9. HALLAZGOS CLAVE

1. **Predominio femenino**: {sexo_count.get("Femenino", 0)} de {n} casos ({sexo_count.get("Femenino", 0)/n*100:.1f}%) son mujeres
2. **Población joven en edad productiva**: Edad promedio {edad_prom:.1f} años (rango {edad_min}-{edad_max}), consistente con población maquiladora
3. **IMSS principal notificador**: {inst_count.get("IMSS Ordinario", 0)} casos ({inst_count.get("IMSS Ordinario", 0)/n*100:.1f}%) notificados por IMSS Ordinario
4. **UMF 44 como principal unidad**: {umf_count.get("44", 0)} casos ({umf_count.get("44", 0)/n*100:.1f}%) adscritos a UMF 44
5. **Dispersión comunitaria**: {len(set(colonias))} colonias afectadas en radio de {max_dist:.1f} km
6. **Oportunidad de atención**: Promedio de {intervalo_prom:.1f} días entre síntomas y atención médica

---

## 10. ARCHIVOS GENERADOS

| Archivo | Descripción |
|---------|-------------|
| `casos_tabla_coordenadas.csv` | CSV con coordenadas georreferenciadas |
| `casos_tabla.json` | Datos completos en formato JSON |
| `casos_tabla.geojson` | GeoJSON para uso en SIG/visor GIS |
| `casos_tabla_mapa.html` | Mapa interactivo Leaflet |
| `analisis_brote_sama.md` | Este documento de análisis |

---

*Análisis generado automáticamente a partir de los datos de la tabla de casos confirmados.*
"""

# --- 3. Save analysis report ---
report_path = os.path.join(DEST_DIR, "analisis_brote_sama.md")
with open(report_path, "w", encoding="utf-8") as f:
    f.write(report)
print(f"[OK] Analisis guardado: {report_path}")

# --- 4. Copy data files ---
files_to_copy = [
    "casos_tabla_coordenadas.csv",
    "casos_tabla.json",
    "casos_tabla.geojson",
    "casos_tabla_mapa.html",
]

for fname in files_to_copy:
    src = os.path.join(SRC_DIR, fname)
    dst = os.path.join(DEST_DIR, fname)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"[OK] Copiado: {fname}")
    else:
        print(f"[ERR] No encontrado: {fname}")

# --- 5. Generate analysis JSON summary ---
analysis_summary = {
    "titulo": "Brote Sarampión Maquiladora SAMA - OOAD Durango",
    "fecha_analisis": datetime.now().isoformat(),
    "total_casos": n,
    "periodo": {
        "inicio": fecha_min.strftime("%d/%m/%Y"),
        "fin": fecha_max.strftime("%d/%m/%Y"),
        "dias": (fecha_max - fecha_min).days + 1
    },
    "demograficos": {
        "edad_promedio": round(edad_prom, 1),
        "edad_mediana": edad_mediana,
        "edad_min": edad_min,
        "edad_max": edad_max,
        "sexo": dict(sexo_count),
        "razon_mf": round(sexo_count.get("Masculino", 0)/sexo_count.get("Femenino", 1), 2)
    },
    "instituciones": dict(inst_count),
    "umf": dict(umf_count),
    "colonias_afectadas": len(set(colonias)),
    "colonias": dict(colonia_count),
    "curva_epidemica": [{"fecha": f, "casos": c} for f, c in curva_sorted],
    "oportunidad_atencion": {
        "promedio_dias": round(intervalo_prom, 1),
        "min_dias": min(intervalos),
        "max_dias": max(intervalos)
    },
    "geografia": {
        "centro_lat": round(lat_centro, 4),
        "centro_lng": round(lng_centro, 4),
        "dispersion_max_km": round(max_dist, 2)
    },
    "grupos_edad": grupo_count
}

summary_path = os.path.join(DEST_DIR, "resumen_analisis_brote.json")
with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(analysis_summary, f, ensure_ascii=False, indent=2)
print(f"[OK] Resumen JSON guardado: {summary_path}")

# --- 6. List final contents ---
print("\n[DIR] Contenido final de la carpeta:")
for f in sorted(os.listdir(DEST_DIR)):
    size = os.path.getsize(os.path.join(DEST_DIR, f))
    print(f"   {f} ({size:,} bytes)")

print("\n[OK] Analisis y archivos guardados exitosamente.")
