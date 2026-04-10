import os
import json
import re

py_file = r"c:\Users\aicil\OneDrive\Escritorio\PVU\tablero-sarampion-v2\actualizar_y_publicar.py"
metas_file = r"C:\Users\aicil\.gemini\antigravity\scratch\metadatos_completos.py"
out_file = py_file

with open(metas_file, "r", encoding="utf-8") as f:
    metas_code = f.read()

with open(py_file, "r", encoding="utf-8") as f:
    code = f.read()

code = re.sub(r'METAS_MUNICIPIOS\s*=\s*\{.*?\}\n\n', '', code, flags=re.DOTALL)
code = re.sub(r'DATOS_EXCEL\s*=\s*\{.*?\}\n\n', '', code, flags=re.DOTALL)

insert_point = code.find("# ──────────────────────────────────────────────────\n# 3. CONSTRUIR")
new_code = code[:insert_point] + metas_code + "\n\n" + code[insert_point:]

html_generation_replacement = """# ──────────────────────────────────────────────────
# 3. CONSTRUIR EL HTML Y TABLAS POR MUNICIPIO
# ──────────────────────────────────────────────────
import unicodedata

def normalize_text(text):
    if not text: return ""
    text = str(text).strip().upper()
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

def fmt(n):
    return f"{int(n):,}".replace(",", ",")

def pct(p, s):
    tot = p + s
    return round(p / tot * 100) if tot else 50
    
def get_semaforo(val):
    if val >= 95: return "✅ META", "badge-verde"
    elif val >= 80: return "🟢 BUENA", "badge-verde"
    elif val >= 50: return "🟡 PROCESO", "badge-amarillo"
    elif val >= 25: return "🟠 BAJA", "badge-naranja"
    else: return "🔴 CRÍTICO", "badge-rojo"

def render_tabla_municipios(df_src, cols_sum, meta_dict):
    if not cols_sum:
        return ""
    
    valid_cols = [c for c in cols_sum if c in df_src.columns]
    mun_df = df_src.groupby("MUNICIPIO")[valid_cols].sum().reset_index()
    mun_df["nominal"] = mun_df[valid_cols].sum(axis=1)
    
    filas = []
    for _, r in mun_df.iterrows():
        m_name = str(r["MUNICIPIO"]).strip()
        m_norm = normalize_text(m_name)
        if m_norm == "PUEBLO NUEVO DGO": m_norm = "PUEBLO NUEVO"
        
        datos = meta_dict.get(m_norm, {"name": m_name.title(), "u": 0, "p": "-", "m": 0, "c": 0})
        m_display = datos.get("name", m_name.title()) 
        universo = datos["u"]
        pct_meta = datos["p"]
        meta_sect = datos["m"]
        cubos = datos["c"]
        nominal = int(r["nominal"])
        total_dosis = cubos + nominal
        pendientes = max(0, meta_sect - total_dosis)
        
        cob_val = (total_dosis / meta_sect * 100) if meta_sect > 0 else 0
        
        filas.append((m_display, universo, pct_meta, meta_sect, cubos, nominal, total_dosis, pendientes, cob_val))
    
    filas.sort(key=lambda x: x[6], reverse=True)
    
    html = '''<div class="table-wrapper" style="margin-top:20px;">
        <table>
          <thead><tr><th>#</th><th>Municipio</th><th>Universo 2026</th><th>% Meta</th><th>Meta Sect.</th><th>Cubos Ene-May</th><th>Nominal Jun-Abr</th><th>Total Dosis</th><th>Pendientes</th><th>Cobertura</th><th>Semáforo</th></tr></thead>
          <tbody>'''
          
    for i, (m_display, universo, pct_meta, meta_sect, cubos, nominal, total_dosis, pendientes, cob_val) in enumerate(filas):
        sem_text, bg_class = get_semaforo(cob_val)
        c_str = f"{cob_val:.1f}%" if meta_sect > 0 else "0.0%"
        m_str = fmt(meta_sect) if meta_sect > 0 else "-"
        u_str = fmt(universo) if universo > 0 else "-"
        
        html += f'''
        <tr>
          <td>{i+1}</td>
          <td style="font-weight:700">{m_display}</td>
          <td>{u_str}</td>
          <td>{pct_meta}</td>
          <td style="font-weight:700;color:#6b7280;">{m_str}</td>
          <td>{fmt(cubos)}</td>
          <td>{fmt(nominal)}</td>
          <td class="badge-num" style="background-color:#dbeafe; color:#1e40af;">{fmt(total_dosis)}</td>
          <td style="color:#b91c1c;">{fmt(pendientes)}</td>
          <td style="font-weight:800;color:#1e3a5f;">{c_str}</td>
          <td><span class="hero-badge {bg_class}" style="margin:0;padding:2px 8px;font-size:0.7rem;">{sem_text}</span></td>
        </tr>'''
        
    html += "</tbody></table></div>"
    return html

resumen_filas = []
mun_global = df.groupby("MUNICIPIO").agg({
    "SRP  PRIMERA TOTAL": "sum", "SRP SEGUNDA TOTAL": "sum",
    "SR PRIMERA TOTAL": "sum", "SR SEGUNDA TOTAL": "sum"
}).reset_index()
mun_global["nominal"] = mun_global.sum(axis=1, numeric_only=True)

for _, r in mun_global.iterrows():
    m_name = str(r["MUNICIPIO"]).strip()
    m_norm = normalize_text(m_name)
    if m_norm == "PUEBLO NUEVO DGO": m_norm = "PUEBLO NUEVO"
    
    datos = DATOS_EXCEL.get("resumen", {}).get(m_norm, {"name": m_name.title(), "u": 0, "p": "-", "m": 0, "c": 0})
    m_display = datos.get("name", m_name.title()) 
    universo = datos["u"]
    pct_meta = datos["p"]
    meta_sect = datos["m"]
    cubos = datos["c"]
    nominal = int(r["nominal"])
    total_dosis = cubos + nominal
    pendientes = max(0, meta_sect - total_dosis)
    cob_val = (total_dosis / meta_sect * 100) if meta_sect > 0 else 0
    
    resumen_filas.append((m_display, universo, pct_meta, meta_sect, cubos, nominal, total_dosis, pendientes, cob_val))

resumen_filas.sort(key=lambda x: x[6], reverse=True)
filas_municipios = ""
for i, m in enumerate(resumen_filas):
    sem_text, bg_class = get_semaforo(m[8])
    c_str = f"{m[8]:.1f}%" if m[3] > 0 else "0.0%"
    m_str = fmt(m[3]) if m[3] > 0 else "-"
    u_str = fmt(m[1]) if m[1] > 0 else "-"
    
    filas_municipios += f'''
        <tr>
          <td>{i+1}</td>
          <td style="font-weight:700">{m[0]}</td>
          <td>{u_str}</td>
          <td>{m[2]}</td>
          <td style="font-weight:700;color:#6b7280;">{m_str}</td>
          <td>{fmt(m[4])}</td>
          <td>{fmt(m[5])}</td>
          <td class="badge-num" style="background-color:#dbeafe; color:#1e40af;">{fmt(m[6])}</td>
          <td style="color:#b91c1c;">{fmt(m[7])}</td>
          <td style="font-weight:800;color:#1e3a5f;">{c_str}</td>
          <td><span class="hero-badge {bg_class}" style="margin:0;padding:2px 8px;font-size:0.7rem;">{sem_text}</span></td>
        </tr>'''

def barra_html(label, primera, segunda, total_g):
"""

match1 = re.search(r"# ──────────────────────────────────────────────────\n# 3. CONSTRUIR EL HTML\s*.*?def barra_html\(label, primera, segunda, total_g\):", new_code, flags=re.DOTALL)

if match1:
    new_code = new_code[:match1.start()] + html_generation_replacement + new_code[match1.end():]
else:
    print("FALLO MATCHING EN REEMPLAZO!")

with open(out_file, "w", encoding="utf-8") as f:
    f.write(new_code)
print("REFACCIÓN COMPLETADA! Acentos eliminados del motor de búsqueda.")
