
# -*- coding: utf-8 -*-
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv(r'C:\SRP\SRP-SR-2025_21-06-2026 08-32-01.csv', encoding='latin-1', low_memory=False)
dur = df[df['ESTADO'].str.upper().str.contains('DURANGO', na=False)].copy()

# Columnas de dosis
dose_cols = [c for c in dur.columns if c.startswith('SRP') or c.startswith('SR ')]
for c in dose_cols:
    dur[c] = pd.to_numeric(dur[c], errors='coerce').fillna(0)

def norm_mun(s):
    if not isinstance(s, str): return ''
    s = s.upper().strip()
    s = s.replace('PEA\x91ON','PENON').replace('PEA ON','PENON')
    return s

dur['MUN_NORM'] = dur['MUNICIPIO'].apply(norm_mun)

# Separar por temporada
dur25 = dur[dur['Temporada'] == 2025].copy()
dur26 = dur[dur['Temporada'] == 2026].copy()

# Agregar por municipio
agg25    = dur25.groupby('MUN_NORM')[dose_cols].sum().sum(axis=1)
agg26    = dur26.groupby('MUN_NORM')[dose_cols].sum().sum(axis=1)
agg_total = dur.groupby('MUN_NORM')[dose_cols].sum().sum(axis=1)

print('=== DOSIS MEZQUITAL ===')
mez25  = int(agg25.get('MEZQUITAL', 0))
mez26  = int(agg26.get('MEZQUITAL', 0))
mez_tot = int(agg_total.get('MEZQUITAL', 0))
print(f'  Temporada 2025: {mez25:,}')
print(f'  Temporada 2026: {mez26:,}')
print(f'  Total CSV:      {mez_tot:,}')

print()
print('=== TOTALES DURANGO ===')
print(f'  2025: {int(agg25.sum()):,}')
print(f'  2026: {int(agg26.sum()):,}')
print(f'  Total: {int(agg_total.sum()):,}')

print()
print('=== TODOS LOS MUNICIPIOS (2025 / 2026 / TOTAL) ===')
for mun in sorted(agg_total.index):
    v25  = int(agg25.get(mun, 0))
    v26  = int(agg26.get(mun, 0))
    vtot = int(agg_total.get(mun, 0))
    print(f'  {mun}: 2025={v25:,}  2026={v26:,}  Total={vtot:,}')
