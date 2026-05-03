
import pandas as pd
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

df = pd.read_csv(r'c:\Descargas_SRP\SRP-SR-2025_28-04-2026 08-14-18.csv', encoding='latin1', sep=';')

num_cols = [c for c in df.columns if c not in ['id','INSTITUCION','DELEGACION','ESTADO','JURISDICCION','MUNICIPIO','CLUES','Fecha de registro','Temporada']]
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

df26 = df[df['Temporada']==2026].copy()
dur26 = df26[df26['ESTADO']=='DURANGO'].copy()

srp_6_11 = 'SRP 6 A 11 MESES PRIMERA'
srp_1a = 'SRP 1 ANIO  PRIMERA'
srp_2_5 = 'SRP 2 A 5 ANIOS PRIMERA'
srp_6a = 'SRP 6 ANIOS PRIMERA'
srp_7_9 = 'SRP 7 A 9 ANIOS PRIMERA'
srp_10_12 = 'SRP 10 A 12 ANIOS PRIMERA'
srp_13_19 = 'SRP 13 A 19 ANIOS PRIMERA'
srp_20_29 = 'SRP 20 A 29 ANIOS PRIMERA'
srp_30_39 = 'SRP 30 A 39 ANIOS PRIMERA'
srp_40_49 = 'SRP 40 A 49 ANIOS PRIMERA'
srp_salud = 'SRP PERSONAL DE SALUD PRIMERA'
srp_educ  = 'SRP PERSONAL EDUCATIVO PRIMERA'
srp_jorn  = 'SRP JORNALEROS AGRICOLAS PRIMERA'
srp_pt    = 'SRP  PRIMERA TOTAL'

srp_18m   = 'SRP 18 MESES SEGUNDA'
srp_2_5_2 = 'SRP 2 A 5 ANIOS SEGUNDA'
srp_st    = 'SRP SEGUNDA TOTAL'

sr_6_11   = 'SR 6 A 11 MESES PRIMERA'
sr_1a     = 'SR 1 ANIO PRIMERA'
sr_2_5    = 'SR 2 A 5 ANIOS PRIMERA'
sr_6a     = 'SR 6 ANIOS PRIMERA'
sr_7_9    = 'SR 7 A 9 ANIOS PRIMERA'
sr_10_12  = 'SR 10 A 12 ANIOS PRIMERA'
sr_13_19  = 'SR 13 A 19 ANIOS PRIMERA'
sr_20_29  = 'SR 20 A 29 ANIOS PRIMERA'
sr_30_39  = 'SR 30 A 39 ANIOS PRIMERA'
sr_40_49  = 'SR 40 A 49 ANIOS PRIMERA'
sr_salud  = 'SR PERSONAL DE SALUD PRIMERA'
sr_educ   = 'SR PERSONAL EDUCATIVO PRIMERA'
sr_jorn   = 'SR JORNALEROS AGRICOLAS PRIMERA'
sr_pt     = 'SR PRIMERA TOTAL'

sr_18m    = 'SR 18 MESES SEGUNDA'
sr_2_5_2  = 'SR 2 A 5 ANIOS SEGUNDA'
sr_st     = 'SR SEGUNDA TOTAL'

JURISDICCIONES = ['DURANGO','GOMEZ PALACIO','SANTIAGO PAPASQUIARO','RODEO']

s_act = 51   # semana actual (18-24 abril 2026)
s_ant = 50   # semana anterior (11-17 abril 2026)

dur_act  = dur26[dur26['SEMANA']==s_act]
dur_ant  = dur26[dur26['SEMANA']==s_ant]
dur_acum = dur26[dur26['SEMANA']<=s_act]
dur_acum_ant = dur26[dur26['SEMANA']<=s_ant]

def tot(data, col):
    return int(data[col].sum())

def tot_jur(data, jur, col):
    sub = data[data['JURISDICCION']==jur]
    return int(sub[col].sum())

# ============================================================
# TABLA 1: Dosis Cero SRP 6-11 meses por jurisdiccion
# ============================================================
print("=== TABLA 1: DOSIS CERO (SRP 6-11 meses) POR JURISDICCION ===")
print(f"{'Jurisdicción':<30} {'Sem Anterior':>13} {'Sem Actual':>11} {'Diferencia':>11} {'Acumulado':>11}")
total_ant_t1 = 0; total_act_t1 = 0; total_acum_t1 = 0
for j in JURISDICCIONES:
    ant  = tot_jur(dur_ant, j, srp_6_11)
    act  = tot_jur(dur_act, j, srp_6_11)
    acum = tot_jur(dur_acum, j, srp_6_11)
    diff = act - ant
    total_ant_t1+=ant; total_act_t1+=act; total_acum_t1+=acum
    print(f"  {j:<28} {ant:>13,} {act:>11,} {diff:>+11,} {acum:>11,}")
print(f"  {'TOTAL ESTATAL':<28} {total_ant_t1:>13,} {total_act_t1:>11,} {total_act_t1-total_ant_t1:>+11,} {total_acum_t1:>11,}")

# ============================================================
# TABLA 2: Primera Dosis SRP por Jurisdiccion y Grupo de Edad (semana actual)
# ============================================================
print("\n=== TABLA 2: PRIMERA DOSIS SRP POR JURISDICCION Y GRUPO DE EDAD ===")
grupos_srp1 = [
    ('6-11m', srp_6_11), ('1 año', srp_1a), ('2-5a', srp_2_5), ('6a', srp_6a),
    ('7-9a', srp_7_9), ('10-12a', srp_10_12), ('13-19a', srp_13_19),
    ('20-29a', srp_20_29), ('30-39a', srp_30_39), ('40-49a', srp_40_49),
    ('Pers.Salud', srp_salud), ('Pers.Educ', srp_educ), ('Jornaleros', srp_jorn), ('TOTAL', srp_pt)
]
header = f"{'Jurisdicción':<22}" + "".join([f"{g[0]:>10}" for g in grupos_srp1])
print(header)
for j in JURISDICCIONES:
    row = f"  {j:<20}"
    for g in grupos_srp1:
        row += f"{tot_jur(dur_act, j, g[1]):>10,}"
    print(row)
# Totales
row_t = f"  {'ESTATAL':<20}"
for g in grupos_srp1:
    row_t += f"{tot(dur_act, g[1]):>10,}"
print(row_t)

# ============================================================
# TABLA 3: Primera Dosis SRP - Comparativo semana ant vs act
# ============================================================
print("\n=== TABLA 3: COMPARATIVO 1a DOSIS SRP INTERSEMANAL ===")
print(f"{'Jurisdicción':<30} {'Sem Ant (11-17 abr)':>20} {'Sem Act (18-24 abr)':>20} {'Diferencia':>12}")
for j in JURISDICCIONES:
    ant = tot_jur(dur_ant, j, srp_pt)
    act = tot_jur(dur_act, j, srp_pt)
    print(f"  {j:<28} {ant:>20,} {act:>20,} {act-ant:>+12,}")
print(f"  {'ESTATAL':<28} {tot(dur_ant, srp_pt):>20,} {tot(dur_act, srp_pt):>20,} {tot(dur_act,srp_pt)-tot(dur_ant,srp_pt):>+12,}")

# ============================================================
# TABLA 4: Segunda Dosis SRP (18m) por Jurisdiccion comparativo
# ============================================================
print("\n=== TABLA 4: SEGUNDA DOSIS SRP (18 meses) COMPARATIVO ===")
print(f"{'Jurisdicción':<30} {'Sem Ant':>10} {'Sem Act':>10} {'Dif':>8} {'Acumulado':>11}")
for j in JURISDICCIONES:
    ant  = tot_jur(dur_ant, j, srp_18m)
    act  = tot_jur(dur_act, j, srp_18m)
    acum = tot_jur(dur_acum, j, srp_18m)
    print(f"  {j:<28} {ant:>10,} {act:>10,} {act-ant:>+8,} {acum:>11,}")
print(f"  {'ESTATAL':<28} {tot(dur_ant,srp_18m):>10,} {tot(dur_act,srp_18m):>10,} {tot(dur_act,srp_18m)-tot(dur_ant,srp_18m):>+8,} {tot(dur_acum,srp_18m):>11,}")

# ============================================================
# TABLA 5: SR Primera Dosis por Jurisdiccion comparativo
# ============================================================
print("\n=== TABLA 5: SR PRIMERA DOSIS COMPARATIVO ===")
print(f"{'Jurisdicción':<30} {'Sem Ant':>10} {'Sem Act':>10} {'Dif':>8} {'Acumulado':>11}")
for j in JURISDICCIONES:
    ant  = tot_jur(dur_ant, j, sr_pt)
    act  = tot_jur(dur_act, j, sr_pt)
    acum = tot_jur(dur_acum, j, sr_pt)
    print(f"  {j:<28} {ant:>10,} {act:>10,} {act-ant:>+8,} {acum:>11,}")
print(f"  {'ESTATAL':<28} {tot(dur_ant,sr_pt):>10,} {tot(dur_act,sr_pt):>10,} {tot(dur_act,sr_pt)-tot(dur_ant,sr_pt):>+8,} {tot(dur_acum,sr_pt):>11,}")

# ============================================================
# TABLA 6: SR Segunda Dosis comparativo
# ============================================================
print("\n=== TABLA 6: SR SEGUNDA DOSIS COMPARATIVO ===")
print(f"{'Jurisdicción':<30} {'Sem Ant':>10} {'Sem Act':>10} {'Dif':>8} {'Acumulado':>11}")
for j in JURISDICCIONES:
    ant  = tot_jur(dur_ant, j, sr_st)
    act  = tot_jur(dur_act, j, sr_st)
    acum = tot_jur(dur_acum, j, sr_st)
    print(f"  {j:<28} {ant:>10,} {act:>10,} {act-ant:>+8,} {acum:>11,}")
print(f"  {'ESTATAL':<28} {tot(dur_ant,sr_st):>10,} {tot(dur_act,sr_st):>10,} {tot(dur_act,sr_st)-tot(dur_ant,sr_st):>+8,} {tot(dur_acum,sr_st):>11,}")

# ============================================================
# TABLA 7: Poblaciones especiales (personal salud, educ, jorn)
# ============================================================
print("\n=== TABLA 7: POBLACIONES ESPECIALES - SRP 1a DOSIS ===")
print(f"{'Jurisdicción':<30} {'Pers.Salud':>11} {'Pers.Educ':>10} {'Jornaleros':>11}")
for j in JURISDICCIONES:
    ps  = tot_jur(dur_act, j, srp_salud)
    pe  = tot_jur(dur_act, j, srp_educ)
    pj  = tot_jur(dur_act, j, srp_jorn)
    print(f"  {j:<28} {ps:>11,} {pe:>10,} {pj:>11,}")
print(f"  {'ESTATAL':<28} {tot(dur_act,srp_salud):>11,} {tot(dur_act,srp_educ):>10,} {tot(dur_act,srp_jorn):>11,}")

# ============================================================
# TABLA 8: Resumen General (SRP+SR acumulado)
# ============================================================
print("\n=== TABLA 8: RESUMEN GENERAL ACUMULADO 2026 ===")
print(f"{'Vacuna':<20} {'1a Dosis Acum':>15} {'2a Dosis Acum':>15} {'Total':>10}")
srp1 = tot(dur_acum, srp_pt)
srp2 = tot(dur_acum, srp_st)
sr1  = tot(dur_acum, sr_pt)
sr2  = tot(dur_acum, sr_st)
print(f"  {'SRP':<18} {srp1:>15,} {srp2:>15,} {srp1+srp2:>10,}")
print(f"  {'SR':<18} {sr1:>15,} {sr2:>15,} {sr1+sr2:>10,}")
print(f"  {'TOTAL ESTATAL':<18} {srp1+sr1:>15,} {srp2+sr2:>15,} {srp1+srp2+sr1+sr2:>10,}")

# ============================================================
# ACUMULADOS PREVIOS (hasta sem ant)
# ============================================================
print("\n=== ACUMULADOS HASTA SEMANA ANTERIOR (sem 50) ===")
srp1_ant = tot(dur_acum_ant, srp_pt)
srp2_ant = tot(dur_acum_ant, srp_st)
sr1_ant  = tot(dur_acum_ant, sr_pt)
sr2_ant  = tot(dur_acum_ant, sr_st)
print(f"SRP 1a: {srp1_ant:,}  SRP 2a: {srp2_ant:,}  SR 1a: {sr1_ant:,}  SR 2a: {sr2_ant:,}")

# ============================================================
# PRIMERA DOSIS SRP POR GRUPO EDAD - ACUMULADO
# ============================================================
print("\n=== 1a DOSIS SRP POR GRUPO EDAD - ACUMULADO ESTATAL ===")
for nombre, col in grupos_srp1[:-1]:
    print(f"  {nombre}: {tot(dur_acum, col):,}")
