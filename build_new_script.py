import os
import json
import re

py_file = r"c:\Users\aicil\OneDrive\Escritorio\PVU\tablero-sarampion-v2\actualizar_y_publicar.py"
metas_file = r"C:\Users\aicil\.gemini\antigravity\scratch\metas_dict.py"
out_file = r"c:\Users\aicil\OneDrive\Escritorio\PVU\tablero-sarampion-v2\actualizar_y_publicar.py"

with open(metas_file, "r", encoding="utf-8") as f:
    metas_code = f.read()

with open(py_file, "r", encoding="utf-8") as f:
    code = f.read()

# Make sure we don't duplicate
if "METAS_MUNICIPIOS" not in code:
    # Insert metas right before the HTML builder
    insert_point = code.find("# ──────────────────────────────────────────────────\n# 3. CONSTRUIR EL HTML")
    new_code = code[:insert_point] + metas_code + "\n\n" + code[insert_point:]
else:
    new_code = code

# Now we need to modify the table generation part!
# Original code has `filas_municipios` and `barras_html`.
# Let's replace the HTML construction entirely from # 3. CONSTRUIR EL HTML, downwards up to the <footer>.

html_generation_replacement = """# ──────────────────────────────────────────────────
# 3. CONSTRUIR EL HTML Y TABLAS POR MUNICIPIO
# ──────────────────────────────────────────────────
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

def render_tabla_municipios(df_src, cols_sum, meta_dict, es_resumen=False):
    # Agrupar
    if not cols_sum:
        return ""
    
    valid_cols = [c for c in cols_sum if c in df_src.columns]
    mun_df = df_src.groupby("MUNICIPIO")[valid_cols].sum().reset_index()
    mun_df["total"] = mun_df[valid_cols].sum(axis=1)
    
    filas = []
    for _, r in mun_df.iterrows():
        m_name = str(r["MUNICIPIO"]).strip()
        m_norm = m_name.upper()
        if m_norm == "PUEBLO NUEVO DGO": m_norm = "PUEBLO NUEVO"
        
        meta = meta_dict.get(m_norm, 0)
        t = int(r["total"])
        cob_val = (t / meta * 100) if meta > 0 else 0
        
        filas.append((m_name, t, meta, cob_val, r))
    
    filas.sort(key=lambda x: x[1], reverse=True)
    
    html = '''<div class="table-wrapper" style="margin-top:20px;">
        <table>
          <thead><tr><th>#</th><th>Municipio</th><th>Dosis</th><th>Meta</th><th>Cobertura</th><th>Semáforo</th></tr></thead>
          <tbody>'''
          
    for i, (m_name, t, meta, cob_val, r) in enumerate(filas):
        sem_text, bg_class = get_semaforo(cob_val)
        c_str = f"{cob_val:.1f}%" if meta > 0 else "0.0%"
        m_str = fmt(meta) if meta > 0 else "-"
        
        html += f'''
        <tr>
          <td>{i+1}</td>
          <td style="font-weight:700">{m_name.title()}</td>
          <td class="badge-num">{fmt(t)}</td>
          <td style="font-weight:700;color:#6b7280;">{m_str}</td>
          <td style="font-weight:800;color:#1e3a5f;">{c_str}</td>
          <td><span class="hero-badge {bg_class}" style="margin:0;padding:2px 8px;font-size:0.7rem;">{sem_text}</span></td>
        </tr>'''
        
    html += "</tbody></table></div>"
    return html

# Generar filas_municipios original (resumen con desglose SRP/SR, modificado para incluir semaforo)
resumen_filas = []
mun_global = df.groupby("MUNICIPIO").agg({
    "SRP  PRIMERA TOTAL": "sum", "SRP SEGUNDA TOTAL": "sum",
    "SR PRIMERA TOTAL": "sum", "SR SEGUNDA TOTAL": "sum"
}).reset_index()
mun_global["total"] = mun_global.sum(axis=1, numeric_only=True)

for _, r in mun_global.iterrows():
    m_name = str(r["MUNICIPIO"]).strip()
    m_norm = m_name.upper()
    if m_norm == "PUEBLO NUEVO DGO": m_norm = "PUEBLO NUEVO"
    
    meta = METAS_MUNICIPIOS.get("resumen", {}).get(m_norm, 0)
    t = int(r["total"])
    cob_val = (t / meta * 100) if meta > 0 else 0
    resumen_filas.append((m_name, int(r["SRP  PRIMERA TOTAL"]), int(r["SRP SEGUNDA TOTAL"]), int(r["SR PRIMERA TOTAL"]), int(r["SR SEGUNDA TOTAL"]), t, meta, cob_val))

resumen_filas.sort(key=lambda x: x[5], reverse=True)
filas_municipios = ""
for i, m in enumerate(resumen_filas):
    sem_text, bg_class = get_semaforo(m[7])
    c_str = f"{m[7]:.1f}%" if m[6] > 0 else "0.0%"
    m_str = fmt(m[6]) if m[6] > 0 else "-"
    filas_municipios += f'''
        <tr>
          <td>{i+1}</td>
          <td style="font-weight:700">{m[0].title()}</td>
          <td>{fmt(m[1])}</td>
          <td>{fmt(m[2])}</td>
          <td>{fmt(m[3])}</td>
          <td>{fmt(m[4])}</td>
          <td class="badge-num">{fmt(m[5])}</td>
          <td style="font-weight:700;color:#6b7280;">{m_str}</td>
          <td style="font-weight:800;color:#1e3a5f;">{c_str}</td>
          <td><span class="hero-badge {bg_class}" style="margin:0;padding:2px 8px;font-size:0.7rem;">{sem_text}</span></td>
        </tr>'''

# Barra visual por grupo
def barra_html(label, primera, segunda, total_g):
    p1 = pct(primera, segunda)
    p2 = 100 - p1
    s1 = f"1ª {fmt(primera)}" if primera else ""
    s2 = f"2ª {fmt(segunda)}" if segunda else ""
    barra = ""
    if primera:
        barra += f'<div class="barra-fill barra-primera" style="width:{p1}%"><span>{s1}</span></div>'
    if segunda:
        barra += f'<div class="barra-fill barra-segunda" style="width:{p2}%"><span>{s2}</span></div>'
    return f'''
      <div class="grupo-barra">
        <div class="grupo-header"><span>{label}</span><span>{fmt(total_g)} dosis</span></div>
        <div class="barra-track">{barra}</div>
      </div>'''

barras_html = ""
for nombre, g in grupos.items():
    total_g = g["primera"] + g["segunda"]
    barras_html += barra_html(nombre.title(), g["primera"], g["segunda"], total_g)

# Tarjetas jurisdicciones
cards_juris = ""
for j in jurisdicciones_js:
    cards_juris += f'''
            <div class="juris-card">
              <div class="juris-name">📍 {j['j'].title()}</div>
              <div class="juris-stat"><span>SRP Primera</span><span class="badge-num">{fmt(j['srp_p'])}</span></div>
              <div class="juris-stat"><span>SRP Segunda</span><span class="badge-num">{fmt(j['srp_s'])}</span></div>
              <div class="juris-stat"><span>SR Primera</span><span class="badge-num">{fmt(j['sr_p'])}</span></div>
              <div class="juris-stat"><span>SR Segunda</span><span class="badge-num">{fmt(j['sr_s'])}</span></div>
              <div class="juris-stat"><span>TOTAL</span><span class="badge-num">{fmt(j['t'])}</span></div>
            </div>'''

semanal_json = json.dumps(semanal_js, ensure_ascii=False)
municipios_json = json.dumps(municipios_js, ensure_ascii=False)

if cobertura >= 95:
    semaforo = "✅ META ALCANZADA"; badge_class = "badge-verde"
elif cobertura >= 80:
    semaforo = "🟢 BUENA COBERTURA"; badge_class = "badge-verde"
elif cobertura >= 50:
    semaforo = "🟡 EN PROCESO"; badge_class = "badge-amarillo"
elif cobertura >= 25:
    semaforo = "🟠 BAJA COBERTURA"; badge_class = "badge-naranja"
else:
    semaforo = "🔴 CRÍTICO"; badge_class = "badge-rojo"

def tab_grupo(icon, label, tab_id, primera, segunda, extra_label="", extra_val="", meta=None, cols_sum=[]):
    total_g = primera + segunda
    ex = f'<div class="metrica-card"><div class="metrica-label">{extra_label}</div><div class="metrica-valor">{extra_val}</div></div>' if extra_label else ""
    
    cob_html = ""
    if meta and meta > 0:
        cob = round((total_g / meta) * 100, 1)
        if cob >= 95:
            sem_text = "✅ META"; bg_class = "badge-verde"
        elif cob >= 80:
            sem_text = "🟢 BUENA"; bg_class = "badge-verde"
        elif cob >= 50:
            sem_text = "🟡 PROCESO"; bg_class = "badge-amarillo"
        elif cob >= 25:
            sem_text = "🟠 BAJA"; bg_class = "badge-naranja"
        else:
            sem_text = "🔴 CRÍTICO"; bg_class = "badge-rojo"
        
        cob_html = f'<div class="metrica-card cobertura" style="border-color:#f59e0b;"><div class="metrica-label">Cobertura (Meta: {fmt(meta)})</div><div class="metrica-valor">{cob}%</div><div class="hero-badge {bg_class}" style="margin-top:0;">{sem_text}</div></div>'
        
    tabla_mun = render_tabla_municipios(df, cols_sum, METAS_MUNICIPIOS.get(tab_id, {}))

    return f'''
      <h3 style="font-size:1rem;font-weight:800;color:#1e3a5f;margin-bottom:16px;">{icon} Grupo {label}</h3>
      <div class="metricas">
        <div class="metrica-card srp"><div class="metrica-label">Primera Dosis</div><div class="metrica-valor">{fmt(primera)}</div></div>
        <div class="metrica-card sr"><div class="metrica-label">Segunda Dosis</div><div class="metrica-valor">{fmt(segunda) if segunda else "N/A"}</div></div>
        <div class="metrica-card total"><div class="metrica-label">Total</div><div class="metrica-valor">{fmt(total_g)}</div></div>
        {cob_html}
        {ex}
      </div>
      <h3 style="font-size:.9rem;font-weight:800;color:#1e3a5f;margin:24px 0 12px;">Cobertura por Municipio</h3>
      {tabla_mun}
      '''

g = grupos
tabs_grupos_html = {
    "g611":  tab_grupo("🍼","6-11 Meses", "g611", g["6-11 meses"]["primera"],   0,         "Segunda Dosis","No aplica", 13899, ["SRP 6 A 11 MESES PRIMERA","SR 6 A 11 MESES PRIMERA"]),
    "g1":    tab_grupo("👶","1 Año (1ª)",   "g1", g["1 año"]["primera"],        0,         "18 Meses (2ª)", fmt(g["1 año"]["segunda"]), 28379, ["SRP 1 ANIO  PRIMERA","SR 1 ANIO PRIMERA","SRP 18 MESES SEGUNDA","SR 18 MESES SEGUNDA"]),
    "g18":   tab_grupo("🧒","18 Meses (2ª)","g18",0, g["18 meses"]["segunda"],  "Primera", "Ver grupo 1 Año", 28379, ["SRP 18 MESES SEGUNDA","SR 18 MESES SEGUNDA"]),
    "grez":  tab_grupo("📚","Rezago 2-12", "grez", g["2-12 años"]["primera"],    g["2-12 años"]["segunda"],  "Grupos","2-5 · 6 · 7-9 · 10-12 años", 179702, ["SRP 2 A 5 ANIOS PRIMERA","SRP 6 ANIOS PRIMERA","SRP 7 A 9 ANIOS PRIMERA","SRP 10 A 12 ANIOS PRIMERA","SR 2 A 5 ANIOS PRIMERA","SR 6 ANIOS PRIMERA","SR 7 A 9 ANIOS PRIMERA","SR 10 A 12 ANIOS PRIMERA","SRP 2 A 5 ANIOS SEGUNDA","SRP 6 ANIOS SEGUNDA","SRP 7 A 9 ANIOS SEGUNDA","SRP 10 A 12 ANIOS SEGUNDA","SR 2 A 5 ANIOS SEGUNDA","SR 6 ANIOS SEGUNDA","SR 7 A 9 ANIOS SEGUNDA","SR 10 A 12 ANIOS SEGUNDA"]),
    "g1319": tab_grupo("🎓","13-19 Años",  "g1319", g["13-19 años"]["primera"],   g["13-19 años"]["segunda"], "Pers. Educativo", fmt(s("SRP PERSONAL EDUCATIVO PRIMERA","SRP  PERSONAL EDUCATIVO SEGUNDA","SR PERSONAL EDUCATIVO PRIMERA","SR PERSONAL EDUCATIVO SEGUNDA")), 123168, ["SRP 13 A 19 ANIOS PRIMERA","SR 13 A 19 ANIOS PRIMERA", "SRP 13 A 19 ANIOS SEGUNDA","SR 13 A 19 ANIOS SEGUNDA"]),
    "g2039": tab_grupo("🧑","20-39 Años",  "g2039", g["20-39 años"]["primera"],   g["20-39 años"]["segunda"], "Pers. Salud", fmt(s("SRP PERSONAL DE SALUD PRIMERA","SRP  PERSONAL DE SALUD SEGUNDA","SR PERSONAL DE SALUD PRIMERA","SR PERSONAL DE SALUD SEGUNDA")), 304407, ["SRP 20 A 29 ANIOS PRIMERA","SRP 30 A 39 ANIOS PRIMERA", "SR 20 A 29 ANIOS PRIMERA","SR 30 A 39 ANIOS PRIMERA","SRP 20 A 29 ANIOS SEGUNDA","SRP 30 A 39 ANIOS SEGUNDA", "SR 20 A 29 ANIOS SEGUNDA","SR 30 A 39 ANIOS SEGUNDA"]),
    "g4049": tab_grupo("👩","40-49 Años",  "g4049", g["40-49 años"]["primera"],   g["40-49 años"]["segunda"], "Jornaleros Agrícolas", fmt(s("SRP JORNALEROS AGRICOLAS PRIMERA","SRP JORNALEROS AGRICOLAS SEGUNDA","SR JORNALEROS AGRICOLAS PRIMERA","SR JORNALEROS AGRICOLAS SEGUNDA")), 112107, ["SRP 40 A 49 ANIOS PRIMERA","SR 40 A 49 ANIOS PRIMERA", "SRP 40 A 49 ANIOS SEGUNDA","SR 40 A 49 ANIOS SEGUNDA"]),
}

# ──────────────────────────────────────────────────
# 4. PLANTILLA HTML COMPLETA
# ──────────────────────────────────────────────────
"""

# Find where the definition of fmt is and slice out everything downwards up to the literal HTML string start
match1 = re.search(r"# ──────────────────────────────────────────────────\n# 3. CONSTRUIR EL HTML\n# ──────────────────────────────────────────────────\ndef fmt\(n\):", new_code)
match2 = re.search(r"# ──────────────────────────────────────────────────\n# 4. PLANTILLA HTML COMPLETA\n# ──────────────────────────────────────────────────\nhtml = f", new_code)

if match1 and match2:
    new_code = new_code[:match1.start()] + html_generation_replacement + new_code[match2.start():]
else:
    print("MATCH FAILED!")

# Replace the HTML Table head for the Resumen
html_table_head_original = "<thead><tr><th>#</th><th>Municipio</th><th>SRP 1ª</th><th>SRP 2ª</th><th>SR 1ª</th><th>SR 2ª</th><th>Total</th></tr></thead>"
html_table_head_new = "<thead><tr><th>#</th><th>Municipio</th><th>SRP 1ª</th><th>SRP 2ª</th><th>SR 1ª</th><th>SR 2ª</th><th>Total</th><th>Meta</th><th>Cob. %</th><th>Semáforo</th></tr></thead>"

new_code = new_code.replace(html_table_head_original, html_table_head_new)

with open(out_file, "w", encoding="utf-8") as f:
    f.write(new_code)
print("Hecho el refactor!")
