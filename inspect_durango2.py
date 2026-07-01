import pandas as pd
from io import StringIO

csv_path = r'C:\Users\aicil\.gemini\antigravity-ide\scratch\SRP-SR-2025_02-04-2026 10-40-30.csv'
with open(csv_path, 'r', encoding='latin1') as f:
    content = f.read()
lines = content.split('\n')
fixed = []
for line in lines:
    line = line.strip()
    if line.startswith('"') and line.endswith('"'):
        line = line[1:-1].replace('""', '"')
    fixed.append(line)
df = pd.read_csv(StringIO('\n'.join(fixed)), encoding='latin1', low_memory=False)
df.columns = df.columns.str.strip()
df['Fecha de registro'] = pd.to_datetime(df['Fecha de registro'], errors='coerce')
dur = df[(df['ESTADO']=='DURANGO') & (df['Temporada']==2026)].copy()

num_cols = [c for c in df.columns if c not in ['id','INSTITUCION','DELEGACION','ESTADO','JURISDICCION','MUNICIPIO','CLUES','Fecha de registro','Temporada','SEMANA']]
for c in num_cols:
    dur[c] = pd.to_numeric(dur[c], errors='coerce').fillna(0)

JURS = ['DURANGO','GOMEZ PALACIO','SANTIAGO PAPASQUIARO','RODEO']
print('=== SEMANAS DISPONIBLES ===')
print(sorted(dur['SEMANA'].unique()))
print()
last_sem = int(dur['SEMANA'].max())
prev_sem = last_sem - 1
print('Semana actual:', last_sem, '  Semana anterior:', prev_sem)
print()
for jur in JURS:
    j_cur = dur[(dur['JURISDICCION']==jur) & (dur['SEMANA']==last_sem)]
    srp_1 = int(j_cur['SRP  PRIMERA TOTAL'].sum())
    srp_2 = int(j_cur['SRP SEGUNDA TOTAL'].sum())
    sr_1  = int(j_cur['SR PRIMERA TOTAL'].sum())
    sr_2  = int(j_cur['SR SEGUNDA TOTAL'].sum())
    print(jur + ': SRP1a=' + str(srp_1) + ' SRP2a=' + str(srp_2) + ' SR1a=' + str(sr_1) + ' SR2a=' + str(sr_2))
