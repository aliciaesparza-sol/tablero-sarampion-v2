import pandas as pd

df = pd.read_csv(r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\CAMPAÑA SARAMPIÓN 10 SEMANAS\SRP-SR-2025_22-02-2026 06-41-08.csv')
ssa = df[(df['INSTITUCION'] == 'SSA') & (df['ESTADO'] == 'DURANGO')]

print("Target: 8418 (40-49 age group)")
print("SSA 40-49 SR Prim:", ssa['SR 40 A 49 ANIOS PRIMERA'].sum())
print("SSA 40-49 SR Seg:", ssa['SR 40 A 49 ANIOS SEGUNDA'].sum())
print("SSA 40-49 SRP Prim:", ssa['SRP 40 A 49 ANIOS PRIMERA'].sum())
print("SSA 40-49 SRP Seg:", ssa['SRP 40 A 49 ANIOS SEGUNDA'].sum())

print("\nCombined:")
print("SR Prim + Seg:", ssa['SR 40 A 49 ANIOS PRIMERA'].sum() + ssa['SR 40 A 49 ANIOS SEGUNDA'].sum())
print("SR Prim + SRP Prim:", ssa['SR 40 A 49 ANIOS PRIMERA'].sum() + ssa['SRP 40 A 49 ANIOS PRIMERA'].sum())
print("All 4 types:", ssa[['SR 40 A 49 ANIOS PRIMERA', 'SR 40 A 49 ANIOS SEGUNDA', 'SRP 40 A 49 ANIOS PRIMERA', 'SRP 40 A 49 ANIOS SEGUNDA']].sum().sum())

print("\nWhat about other age groups for 13-19 (Target 1308)?")
c13 = ['SR 13 A 19 ANIOS PRIMERA', 'SR 13 A 19 ANIOS SEGUNDA', 'SRP 13 A 19 ANIOS PRIMERA', 'SRP 13 A 19 ANIOS SEGUNDA']
for c in c13:
    print(f"  {c}: {ssa[c].sum()}")

print("\nCould 1308 be a sum of multiple?")
print("  SR 13-19 Prim + SRP 13-19 Prim:", ssa['SR 13 A 19 ANIOS PRIMERA'].sum() + ssa['SRP 13 A 19 ANIOS PRIMERA'].sum())
