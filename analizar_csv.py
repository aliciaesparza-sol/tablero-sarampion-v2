
import pandas as pd

df = pd.read_csv(r'c:\Descargas_SRP\SRP-SR-2025_28-04-2026 08-14-18.csv', encoding='latin1', sep=';')

num_cols = [c for c in df.columns if c not in ['id','INSTITUCION','DELEGACION','ESTADO','JURISDICCION','MUNICIPIO','CLUES','Fecha de registro','Temporada']]
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

df['Fecha_dt'] = pd.to_datetime(df['Fecha de registro'], dayfirst=True, errors='coerce')

# Semana 50 = semana anterior (13-19 abril), semana 51 = semana actual (20-24 abril)
# Verifiquemos con Durango
df26 = df[df['Temporada']==2026].copy()
dur26 = df26[df26['ESTADO']=='DURANGO']

srp_1a = 'SRP 1 ANIO  PRIMERA'
srp_pt = 'SRP  PRIMERA TOTAL'
srp_st = 'SRP SEGUNDA TOTAL'
sr_pt = 'SR PRIMERA TOTAL'
sr_st = 'SR SEGUNDA TOTAL'

# ====== SEMANA ACTUAL (51) ======
s_act = 51
s_ant = 50

# Todo el estado de Durango
dur_act = dur26[dur26['SEMANA']==s_act]
dur_ant = dur26[dur26['SEMANA']==s_ant]

print('=== SEMANA ACTUAL (51 = 20-24 abril 2026) - DURANGO ===')
print(f'Registros: {len(dur_act)}')
print(f'SRP Primera Total: {dur_act[srp_pt].sum():.0f}')
print(f'SRP Segunda Total: {dur_act[srp_st].sum():.0f}')
print(f'SR Primera Total: {dur_act[sr_pt].sum():.0f}')
print(f'SR Segunda Total: {dur_act[sr_st].sum():.0f}')

print('\n=== SEMANA ANTERIOR (50 = 13-19 abril 2026) - DURANGO ===')
print(f'Registros: {len(dur_ant)}')
print(f'SRP Primera Total: {dur_ant[srp_pt].sum():.0f}')
print(f'SRP Segunda Total: {dur_ant[srp_st].sum():.0f}')
print(f'SR Primera Total: {dur_ant[sr_pt].sum():.0f}')
print(f'SR Segunda Total: {dur_ant[sr_st].sum():.0f}')

# ====== ACUMULADO 2026 (todas semanas hasta 51) ======
dur_acum = dur26[dur26['SEMANA']<=s_act]
print('\n=== ACUMULADO 2026 hasta semana 51 - DURANGO ===')
print(f'SRP Primera Total: {dur_acum[srp_pt].sum():.0f}')
print(f'SRP Segunda Total: {dur_acum[srp_st].sum():.0f}')
print(f'SR Primera Total: {dur_acum[sr_pt].sum():.0f}')
print(f'SR Segunda Total: {dur_acum[sr_st].sum():.0f}')

# ====== POR JURISDICCION - SEMANA ACTUAL ======
print('\n=== POR JURISDICCION - SEMANA 51 ===')
jur_act = dur_act.groupby('JURISDICCION').agg({srp_pt:'sum', srp_st:'sum', sr_pt:'sum', sr_st:'sum'}).reset_index()
jur_act['TOTAL_SRP'] = jur_act[srp_pt] + jur_act[srp_st]
jur_act['TOTAL_SR'] = jur_act[sr_pt] + jur_act[sr_st]
jur_act['GRAN_TOTAL'] = jur_act['TOTAL_SRP'] + jur_act['TOTAL_SR']
print(jur_act.to_string())

print('\n=== POR JURISDICCION - SEMANA 50 ===')
jur_ant = dur_ant.groupby('JURISDICCION').agg({srp_pt:'sum', srp_st:'sum', sr_pt:'sum', sr_st:'sum'}).reset_index()
jur_ant['TOTAL_SRP'] = jur_ant[srp_pt] + jur_ant[srp_st]
jur_ant['TOTAL_SR'] = jur_ant[sr_pt] + jur_ant[sr_st]
jur_ant['GRAN_TOTAL'] = jur_ant['TOTAL_SRP'] + jur_ant['TOTAL_SR']
print(jur_ant.to_string())

# ====== ACUMULADO POR JURISDICCION ======
print('\n=== ACUMULADO 2026 POR JURISDICCION ===')
jur_acum = dur_acum.groupby('JURISDICCION').agg({srp_pt:'sum', srp_st:'sum', sr_pt:'sum', sr_st:'sum'}).reset_index()
jur_acum['TOTAL_SRP'] = jur_acum[srp_pt] + jur_acum[srp_st]
jur_acum['TOTAL_SR'] = jur_acum[sr_pt] + jur_acum[sr_st]
jur_acum['GRAN_TOTAL'] = jur_acum['TOTAL_SRP'] + jur_acum['TOTAL_SR']
print(jur_acum.to_string())
