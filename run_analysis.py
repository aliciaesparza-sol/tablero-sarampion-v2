import pandas as pd
import numpy as np
import json

# ---- Stock data ----
stock_file = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\EXISTENCIAS SRP Y SR\EXISTENCIAS_SRP_SR_POR_DIA.xlsx"
df_stock_raw = pd.read_excel(stock_file, sheet_name='Detalle por Jurisdicción')

def parse_date(d):
    try:
        return pd.to_datetime(d, dayfirst=True)
    except:
        return pd.NaT

df_stock_raw['FECHA_PARSED'] = df_stock_raw['FECHA'].apply(parse_date)
df_stock_raw['SECCIÓN'] = df_stock_raw['SECCIÓN'].astype(str).str.strip()

def normalize_jur(s):
    s = s.upper().strip()
    if 'NO. 1' in s or 'NO.1' in s or (s.endswith('1') and 'JURIS' in s): return 'JUR1'
    if 'NO. 2' in s or 'NO.2' in s or (s.endswith('2') and 'JURIS' in s): return 'JUR2'
    if 'NO. 3' in s or 'NO.3' in s or (s.endswith('3') and 'JURIS' in s): return 'JUR3'
    if 'NO. 4' in s or 'NO.4' in s or (s.endswith('4') and 'JURIS' in s): return 'JUR4'
    return None

df_stock_raw['JUR'] = df_stock_raw['SECCIÓN'].apply(normalize_jur)
df_jur = df_stock_raw[df_stock_raw['JUR'].notna() & df_stock_raw['FECHA_PARSED'].notna()].copy()
df_jur = df_jur.sort_values(['JUR', 'FECHA_PARSED'])
df_jur['CONSUMO_SR'] = df_jur.groupby('JUR')['SR PUNTOS'].diff().mul(-1)
df_jur['CONSUMO_SRP'] = df_jur.groupby('JUR')['SRP PUNTOS'].diff().mul(-1)

# ---- Applied doses ----
csv_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\REPORTE_SRP-SR-CENSIA\SRP-SR-2025_14-03-2026 06-41-16.csv"
df_doses = pd.read_csv(csv_path, usecols=[
    'JURISDICCION', 'Fecha de registro',
    'SR PRIMERA TOTAL', 'SR SEGUNDA TOTAL',
    'SRP  PRIMERA TOTAL', 'SRP SEGUNDA TOTAL'
])
df_doses['FECHA_PARSED'] = pd.to_datetime(df_doses['Fecha de registro'], errors='coerce')
df_doses = df_doses[df_doses['FECHA_PARSED'].dt.year >= 2026]
df_doses['SR_APLICADAS'] = df_doses[['SR PRIMERA TOTAL', 'SR SEGUNDA TOTAL']].fillna(0).sum(axis=1)
df_doses['SRP_APLICADAS'] = df_doses[['SRP  PRIMERA TOTAL', 'SRP SEGUNDA TOTAL']].fillna(0).sum(axis=1)

csv_jur_map = {
    'DURANGO': 'JUR1', 'SANTIAGO PAPASQUIARO': 'JUR2', 'RODEO': 'JUR3'
}
def map_jur_csv(j):
    j = str(j).strip().upper()
    for k, v in csv_jur_map.items():
        if k in j: return v
    return None

df_doses['JUR'] = df_doses['JURISDICCION'].apply(map_jur_csv)
doses_agg = df_doses[df_doses['JUR'].notna()].groupby(['FECHA_PARSED', 'JUR']).agg(
    SR_APLICADAS=('SR_APLICADAS', 'sum'),
    SRP_APLICADAS=('SRP_APLICADAS', 'sum')
).reset_index()

# ---- Merge ----
merged = pd.merge(
    df_jur[['FECHA_PARSED', 'JUR', 'SR PUNTOS', 'SRP PUNTOS', 'CONSUMO_SR', 'CONSUMO_SRP']],
    doses_agg[['FECHA_PARSED', 'JUR', 'SR_APLICADAS', 'SRP_APLICADAS']],
    on=['FECHA_PARSED', 'JUR'],
    how='left'
).fillna(0)

merged['SR_APLICADAS'] = merged['SR_APLICADAS'].astype(int)
merged['SRP_APLICADAS'] = merged['SRP_APLICADAS'].astype(int)
merged['CONSUMO_SR'] = merged['CONSUMO_SR'].fillna(0).astype(int)
merged['CONSUMO_SRP'] = merged['CONSUMO_SRP'].fillna(0).astype(int)
merged['DIFER_SR'] = merged['CONSUMO_SR'] - merged['SR_APLICADAS']
merged['DIFER_SRP'] = merged['CONSUMO_SRP'] - merged['SRP_APLICADAS']
merged['FECHA_STR'] = merged['FECHA_PARSED'].dt.strftime('%d/%m/%Y')

# ---- Analysis dict ----
labels = {
    'JUR1': 'Jurisdicción No. 1 (Durango)',
    'JUR2': 'Jurisdicción No. 2 (Santiago Papasquiaro)',
    'JUR3': 'Jurisdicción No. 3 (Rodeo)',
    'JUR4': 'Jurisdicción No. 4'
}

analysis = {}
for jur in ['JUR1', 'JUR2', 'JUR3', 'JUR4']:
    sub = merged[merged['JUR'] == jur].sort_values('FECHA_PARSED')
    if sub.empty:
        analysis[jur] = {'error': 'No data'}
        continue
    analysis[jur] = {
        'label': labels.get(jur, jur),
        'dias': len(sub),
        'sr': {
            'total_aplicadas': int(sub['SR_APLICADAS'].sum()),
            'total_consumo_teorico': int(sub['CONSUMO_SR'].sum()),
            'stock_inicial': int(sub.iloc[0]['SR PUNTOS']),
            'stock_final': int(sub.iloc[-1]['SR PUNTOS']),
            'max_uno_dia': int(sub['SR_APLICADAS'].max()),
            'fecha_max': sub.loc[sub['SR_APLICADAS'].idxmax(), 'FECHA_STR'],
            'dias_sin_aplicacion': int((sub['SR_APLICADAS'] == 0).sum()),
            'desfase_total': int(sub['DIFER_SR'].sum()),
            'desfase_abs_medio': float(round(sub['DIFER_SR'].abs().mean(), 1)),
            'fechas_desfase_alto': sub[sub['DIFER_SR'].abs() > 100]['FECHA_STR'].tolist()
        },
        'srp': {
            'total_aplicadas': int(sub['SRP_APLICADAS'].sum()),
            'total_consumo_teorico': int(sub['CONSUMO_SRP'].sum()),
            'stock_inicial': int(sub.iloc[0]['SRP PUNTOS']),
            'stock_final': int(sub.iloc[-1]['SRP PUNTOS']),
            'max_uno_dia': int(sub['SRP_APLICADAS'].max()),
            'fecha_max': sub.loc[sub['SRP_APLICADAS'].idxmax(), 'FECHA_STR'],
            'dias_sin_aplicacion': int((sub['SRP_APLICADAS'] == 0).sum()),
            'desfase_total': int(sub['DIFER_SRP'].sum()),
            'desfase_abs_medio': float(round(sub['DIFER_SRP'].abs().mean(), 1)),
            'fechas_desfase_alto': sub[sub['DIFER_SRP'].abs() > 100]['FECHA_STR'].tolist()
        }
    }

# Totals all state
total = {
    'sr_total_aplicadas': int(merged['SR_APLICADAS'].sum()),
    'srp_total_aplicadas': int(merged['SRP_APLICADAS'].sum()),
    'total_dosis': int(merged['SR_APLICADAS'].sum() + merged['SRP_APLICADAS'].sum()),
    'periodo': f"{merged['FECHA_PARSED'].min().strftime('%d/%m/%Y')} - {merged['FECHA_PARSED'].max().strftime('%d/%m/%Y')}",
    'dias': merged['FECHA_PARSED'].nunique(),
}
analysis['TOTAL_ESTADO'] = total

with open('C:\\Users\\aicil\\.gemini\\antigravity\\scratch\\analysis.json', 'w', encoding='utf-8') as f:
    json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)

# also export timeseries per jur for charts
merged.to_csv('C:\\Users\\aicil\\.gemini\\antigravity\\scratch\\merged_data.csv', index=False)
print("Done")
print(json.dumps(total, indent=2, ensure_ascii=False))
