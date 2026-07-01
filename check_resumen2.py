
# -*- coding: utf-8 -*-
"""
Verifica las dosis 2026 por municipio usando solo las columnas del tablero
y compara con los valores actuales en el RESUMEN MUNICIPIOS
"""
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv(r'C:\SRP\SRP-SR-2025_21-06-2026 08-32-01.csv', encoding='latin-1', low_memory=False)
dur = df[df['ESTADO'].str.upper().str.contains('DURANGO', na=False)].copy()

# Solo temporada 2026
dur26 = dur[dur['Temporada'] == 2026].copy()
print(f'Registros Durango 2026: {len(dur26)}')

# Columnas del tablero
grupos_cols = {
    '6-11 Meses':  ['SRP 6 A 11 MESES PRIMERA', 'SR 6 A 11 MESES PRIMERA'],
    '1 Anio':      ['SRP 1 ANIO  PRIMERA', 'SR 1 ANIO PRIMERA'],
    '18 Meses':    ['SRP 18 MESES SEGUNDA', 'SR 18 MESES SEGUNDA'],
    '6 Anios':     ['SRP 6 ANIOS PRIMERA', 'SRP 6 ANIOS SEGUNDA', 'SR 6 ANIOS PRIMERA', 'SR 6 ANIOS SEGUNDA'],
    '2-12 Anios':  ['SRP 2 A 5 ANIOS PRIMERA', 'SRP 2 A 5 ANIOS SEGUNDA',
                    'SRP 7 A 9 ANIOS PRIMERA', 'SRP 7 A 9 ANIOS SEGUNDA',
                    'SRP 10 A 12 ANIOS PRIMERA', 'SRP 10 A 12 ANIOS SEGUNDA',
                    'SR 2 A 5 ANIOS PRIMERA', 'SR 2 A 5 ANIOS SEGUNDA',
                    'SR 7 A 9 ANIOS PRIMERA', 'SR 7 A 9 ANIOS SEGUNDA',
                    'SR 10 A 12 ANIOS PRIMERA', 'SR 10 A 12 ANIOS SEGUNDA'],
    '13-19 Anios': ['SRP 13 A 19 ANIOS PRIMERA', 'SRP 13 A 19 ANIOS SEGUNDA',
                    'SR 13 A 19 ANIOS PRIMERA', 'SR 13 A 19 ANIOS SEGUNDA'],
    '20-39 Anios': ['SRP 20 A 29 ANIOS PRIMERA', 'SRP 20 A 29 ANIOS SEGUNDA',
                    'SRP 30 A 39 ANIOS PRIMERA', 'SRP 30 A 39 ANIOS SEGUNDA',
                    'SR 20 A 29 ANIOS PRIMERA', 'SR 20 A 29 ANIOS SEGUNDA',
                    'SR 30 A 39 ANIOS PRIMERA', 'SR 30 A 39 ANIOS SEGUNDA'],
    '40-49 Anios': ['SRP 40 A 49 ANIOS PRIMERA', 'SRP 40 A 49 ANIOS SEGUNDA',
                    'SR 40 A 49 ANIOS PRIMERA', 'SR 40 A 49 ANIOS SEGUNDA'],
}

todas_cols = list(set(c for cols in grupos_cols.values() for c in cols))

for c in todas_cols:
    if c in dur26.columns:
        dur26[c] = pd.to_numeric(dur26[c], errors='coerce').fillna(0)

dur26['MUN_NORM'] = dur26['MUNICIPIO'].str.upper().str.strip()

cols_existentes = [c for c in todas_cols if c in dur26.columns]
agg26 = dur26.groupby('MUN_NORM')[cols_existentes].sum().sum(axis=1)

print()
print('=== DOSIS 2026 POR MUNICIPIO (columnas del tablero) ===')
for mun in sorted(agg26.index):
    v = int(agg26.get(mun, 0))
    print(f'  {mun}: {v:,}')

print()
mez_v = int(agg26.get('MEZQUITAL', 0))
print(f'MEZQUITAL 2026 (tablero): {mez_v:,}')
print(f'TOTAL DURANGO 2026 (tablero): {int(agg26.sum()):,}')

# Ahora comparar con lo que estaba en el RESUMEN original (temporada 2026)
# Original Mezquital Nom 2026 = 23,132 (al 11 junio)
# Nuevo deberia ser el valor al 21 de junio

# Ver cuantos registros tiene Mezquital en 2026
mez26 = dur26[dur26['MUN_NORM'] == 'MEZQUITAL']
print()
print(f'Registros Mezquital 2026: {len(mez26)}')
print('Columnas de dosis Mezquital 2026 por columna:')
for c in sorted(cols_existentes):
    v = int(mez26[c].sum())
    if v > 0:
        print(f'  {c}: {v:,}')
