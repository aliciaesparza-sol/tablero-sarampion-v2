
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from docx import Document
from docx.shared import Pt

# Cargar datos
df = pd.read_csv(r'c:\Descargas_SRP\SRP-SR-2025_28-04-2026 08-14-18.csv', encoding='latin1', sep=';')
num_cols = [c for c in df.columns if c not in ['id','INSTITUCION','DELEGACION','ESTADO','JURISDICCION','MUNICIPIO','CLUES','Fecha de registro','Temporada']]
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

dur26 = df[(df['Temporada']==2026) & (df['ESTADO']=='DURANGO')].copy()

C = {
    'srp_6_11': 'SRP 6 A 11 MESES PRIMERA',
    'srp_pt':   'SRP  PRIMERA TOTAL',
    'srp_18m':  'SRP 18 MESES SEGUNDA',
    'srp_st':   'SRP SEGUNDA TOTAL',
    'sr_pt':    'SR PRIMERA TOTAL',
    'sr_st':    'SR SEGUNDA TOTAL',
}

JURS = ['DURANGO','GOMEZ PALACIO','SANTIAGO PAPASQUIARO','RODEO']
JL = {'DURANGO':'Durango','GOMEZ PALACIO':'Gómez Palacio','SANTIAGO PAPASQUIARO':'Santiago Papasquiaro','RODEO':'Rodeo'}

da   = dur26[dur26['SEMANA']==51]
dant = dur26[dur26['SEMANA']==50]
dacu = dur26[dur26['SEMANA']<=51]
daa  = dur26[dur26['SEMANA']<=50]

def v(d,k): return int(d[C[k]].sum())
def vj(d,j,k): return int(d[d['JURISDICCION']==j][C[k]].sum())
def n(x): return f"{x:,}"

# Valores clave
dc_acum_ant = v(daa,'srp_6_11')  # 5,157
dc_acum     = v(dacu,'srp_6_11') # 5,196
dc_dif      = dc_acum - dc_acum_ant  # 39
dc_pct      = dc_dif/dc_acum_ant*100 if dc_acum_ant>0 else 0

s18_acum_ant = v(daa,'srp_18m')  # 6,976
s18_acum     = v(dacu,'srp_18m') # 7,037
s18_dif      = s18_acum - s18_acum_ant  # 61

# Diferencias por jurisdicción para 2a dosis SRP 18m
s18_dif_dur = vj(dacu,'DURANGO','srp_18m') - vj(daa,'DURANGO','srp_18m')
s18_dif_gp  = vj(dacu,'GOMEZ PALACIO','srp_18m') - vj(daa,'GOMEZ PALACIO','srp_18m')
s18_dif_sp  = vj(dacu,'SANTIAGO PAPASQUIARO','srp_18m') - vj(daa,'SANTIAGO PAPASQUIARO','srp_18m')
s18_dif_rod = vj(dacu,'RODEO','srp_18m') - vj(daa,'RODEO','srp_18m')

# Jornaleros acumulados
jorn_gp = int(dur26[dur26['JURISDICCION']=='GOMEZ PALACIO']['SRP JORNALEROS AGRICOLAS PRIMERA'].sum())

print(f"DC acum ant: {dc_acum_ant}, DC acum: {dc_acum}, dif: {dc_dif}, pct: {dc_pct:.2f}%")
print(f"18m acum ant: {s18_acum_ant}, 18m acum: {s18_acum}, dif: {s18_dif}")
print(f"18m dif Durango: {s18_dif_dur}, GP: {s18_dif_gp}, SP: {s18_dif_sp}, Rodeo: {s18_dif_rod}")
print(f"Jornaleros GP: {jorn_gp}")

# Abrir documento
doc = Document(r'C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\CONASABI\EVIDENCIAS CONASABI_24ABRIL2026\DSP_Vacunación_CONASABIAc2_24abril2026_ACTUALIZADO.docx')

# Función para reemplazar texto completo de un párrafo manteniendo formato del primer run
def replace_para(para, new_text):
    if len(para.runs) == 0:
        return
    # Guardar formato del primer run
    first_run = para.runs[0]
    font_name = first_run.font.name
    font_size = first_run.font.size
    font_bold = first_run.bold
    font_italic = first_run.italic
    font_color = first_run.font.color.rgb if first_run.font.color and first_run.font.color.rgb else None
    
    # Limpiar todos los runs
    for run in para.runs:
        run.text = ''
    # Poner texto en el primer run
    para.runs[0].text = new_text

# Corregir párrafos específicos
for i, p in enumerate(doc.paragraphs):
    txt = p.text
    
    # Párrafo 29: "El acumulado estatal pasó de 5,157 dosis (17 de abril) a 5,196 dosis (17 de abril)..."
    # CORRECCIÓN: fechas deben ser 17 de abril → 24 de abril, y datos correctos
    if 'El acumulado estatal pasó de' in txt and '6–11 meses' in txt:
        replace_para(p, 
            f"La aplicación de primera dosis de SRP presenta incremento estatal respecto al corte previo. "
            f"El acumulado estatal pasó de {n(dc_acum_ant)} dosis (17 de abril) a {n(dc_acum)} dosis "
            f"(24 de abril) en el grupo de 6–11 meses, lo que representa un incremento "
            f"de {dc_dif} dosis adicionales ({dc_pct:.2f}%). "
            f"Este comportamiento refleja continuidad en las estrategias de búsqueda activa en localidades prioritarias."
        )
        print(f"  ✅ Párrafo [{i}] corregido: Dosis cero acumulado")
    
    # Párrafo 42: "pasando de 6,976 a 7,037 dosis" - verificar que las fechas estén bien
    if 'segunda dosis SRP (18 meses)' in txt and 'pasando de' in txt:
        replace_para(p,
            f"Por su parte, la aplicación de segunda dosis SRP (18 meses) registró un aumento de {s18_dif} dosis "
            f"adicionales, pasando de {n(s18_acum_ant)} a {n(s18_acum)} dosis, lo que confirma continuidad "
            f"en las acciones de recuperación del esquema básico en menores de dos años. El comportamiento "
            f"intersemanal muestra continuidad operativa en todas las jurisdicciones del estado."
        )
        print(f"  ✅ Párrafo [{i}] corregido: 2a dosis SRP 18m")
    
    # Párrafo 44: "Con corte al 24 de abril de 2026, el grupo de 6 a 11 meses (dosis cero) registra 5,196"
    if 'primera dosis de vacuna SRP muestra' in txt and 'dosis cero' in txt:
        replace_para(p,
            f"La aplicación de primera dosis de vacuna SRP muestra incremento generalizado en la mayoría de los "
            f"grupos etarios y jurisdicciones sanitarias del estado. Con corte al 24 de abril de 2026, "
            f"el grupo de 6 a 11 meses (dosis cero) registra {n(dc_acum)} dosis a nivel estatal, mientras que "
            f"el grupo de 1 año acumula {n(v(dacu,'srp_pt'))} dosis de primera aplicación. "
            f"La distribución por grupo de edad permite identificar las áreas de mayor y menor avance en la "
            f"recuperación del esquema de vacunación."
        )
        print(f"  ✅ Párrafo [{i}] corregido: 1a dosis SRP por grupo")

    # Párrafo 48: Jornaleros agrícolas
    if 'jornaleros agrícolas' in txt.lower() and 'Gómez Palacio' in txt:
        replace_para(p,
            f"Se observa que Gómez Palacio mantiene mayor captación en jornaleros agrícolas ({n(jorn_gp)}), "
            f"mientras que Durango concentra la mayor vacunación institucional. Santiago Papasquiaro y Rodeo "
            f"continúan con rezago operativo, requiriendo reforzamiento de estrategias extramuros y brigadas "
            f"móviles en localidades de alta dispersión geográfica."
        )
        print(f"  ✅ Párrafo [{i}] corregido: Jornaleros")

    # Párrafo 67: "Con corte al 24 de abril de 2026, el acumulado estatal pasó de..."
    if 'segunda dosis de vacuna SRP (18 meses) muestra continuidad' in txt:
        replace_para(p,
            f"La aplicación de segunda dosis de vacuna SRP (18 meses) muestra continuidad en la recuperación "
            f"del esquema básico infantil como parte de las acciones intensivas implementadas para el control "
            f"del brote de sarampión. Con corte al 24 de abril de 2026, el acumulado estatal pasó de "
            f"{n(s18_acum_ant)} dosis registradas al 17 de abril a {n(s18_acum)} dosis al 24 de abril, lo que "
            f"representa un incremento de {s18_dif} dosis adicionales en el período intersemanal."
        )
        print(f"  ✅ Párrafo [{i}] corregido: Sección VI 2a dosis")

    # Párrafos 73-76: Diferencias por jurisdicción 2a dosis
    if 'Mayor incremento en Gómez Palacio' in txt:
        replace_para(p, f"Mayor incremento en Gómez Palacio (↑ {s18_dif_gp} dosis), derivado del fortalecimiento de la búsqueda nominal en unidades de primer nivel.")
        print(f"  ✅ Párrafo [{i}] corregido: GP 2a dosis")
    if 'Incremento destacado en la Jurisdicción Durango' in txt:
        replace_para(p, f"Incremento destacado en la Jurisdicción Durango (↑ {s18_dif_dur} dosis), asociado a operativos intensivos y captación institucional.")
        print(f"  ✅ Párrafo [{i}] corregido: Durango 2a dosis")
    if 'Crecimiento moderado en Santiago Papasquiaro' in txt:
        replace_para(p, f"Crecimiento moderado en Santiago Papasquiaro (↑ {s18_dif_sp} dosis), relacionado con brigadas extramuros en localidades rurales.")
        print(f"  ✅ Párrafo [{i}] corregido: SP 2a dosis")
    if 'Incremento marginal en Rodeo' in txt:
        replace_para(p, f"Incremento marginal en Rodeo (↑ {s18_dif_rod} dosis), manteniéndose como la jurisdicción con menor volumen operativo.")
        print(f"  ✅ Párrafo [{i}] corregido: Rodeo 2a dosis")

    # Cualquier referencia restante a "10 de abril" → "17 de abril" 
    if '10 de abril' in txt:
        for run in p.runs:
            if '10 de abril' in run.text:
                run.text = run.text.replace('10 de abril', '17 de abril')
        print(f"  ✅ Párrafo [{i}] corregido: fecha 10→17 abril")

# Guardar
OUTPUT = r'C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\CONASABI\EVIDENCIAS CONASABI_24ABRIL2026\DSP_Vacunación_CONASABIAc2_24abril2026_ACTUALIZADO.docx'
doc.save(OUTPUT)
print(f"\n✅ Documento corregido y guardado en:\n{OUTPUT}")
