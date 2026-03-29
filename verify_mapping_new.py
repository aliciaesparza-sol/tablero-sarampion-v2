import pandas as pd

df = pd.read_csv(r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\CAMPAÑA SARAMPIÓN 10 SEMANAS\SRP-SR-2025_22-02-2026 06-41-08.csv')
dur = df[df['ESTADO'] == 'DURANGO']

# Excel Feb 22 values:
# 6-11m: 6309
# 1yr: 12335
# 18m: 9107
# 40-49: 18147

def get_sum(query):
    return dur.filter(like=query).fillna(0).sum().sum()

print("ALL INSTITUTIONS (Feb 22 CSV):")
print('6 A 11 MESES:', get_sum('6 A 11 MESES'))
print('1 ANIO:', get_sum('1 ANIO'))
print('18 MESES:', get_sum('18 MESES'))
print('40 A 49 ANIOS:', get_sum('40 A 49 ANIOS'))

# What if it's SSA only?
ssa = dur[dur['INSTITUCION'] == 'SSA']
def get_sum_ssa(query):
    return ssa.filter(like=query).fillna(0).sum().sum()

print("\nSSA ONLY (Feb 22 CSV):")
print('6 A 11 MESES:', get_sum_ssa('6 A 11 MESES'))
print('1 ANIO:', get_sum_ssa('1 ANIO'))
print('18 MESES:', get_sum_ssa('18 MESES'))
print('40 A 49 ANIOS:', get_sum_ssa('40 A 49 ANIOS'))
