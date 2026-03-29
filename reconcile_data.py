import pandas as pd
import numpy as np

# Load data
csv_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO SARAMPION\SRP-SR-2025_21-03-2026 04-30-33.csv'
df = pd.read_csv(csv_path)

# Previous Excel Values (as of Feb 22)
excel_prev = {
    "6 a 11 meses": 4241,
    "1 año": 11339,
    "18 meses": 9122,
    "Rezagados 2 a 12 años": 0,
    "13 a 19 años": 1308,
    "20 a 39 años": 0,
    "40 a 49 años": 8418
}

# Filter for SSA Durango
ssa_dur = df[(df['INSTITUCION'] == 'SSA') & (df['ESTADO'] == 'DURANGO')]

# Define possible column groups
cols_6_11m = ['SRP 6 A 11 MESES PRIMERA', 'SR 6 A 11 MESES PRIMERA']
cols_1yr = ['SRP 1 ANIO  PRIMERA', 'SR 1 ANIO PRIMERA']
cols_18m = ['SRP 18 MESES SEGUNDA', 'SR 18 MESES SEGUNDA']
cols_2_12 = [
    'SRP 2 A 5 ANIOS PRIMERA', 'SRP 6 ANIOS PRIMERA', 'SRP 7 A 9 ANIOS PRIMERA', 'SRP 10 A 12 ANIOS PRIMERA',
    'SRP 2 A 5 ANIOS SEGUNDA', 'SRP 6 ANIOS SEGUNDA', 'SRP 7 A 9 ANIOS SEGUNDA', 'SRP 10 A 12 ANIOS SEGUNDA',
    'SR 2 A 5 ANIOS PRIMERA', 'SR 6 ANIOS PRIMERA', 'SR 7 A 9 ANIOS PRIMERA', 'SR 10 A 12 ANIOS PRIMERA',
    'SR 2 A 5 ANIOS SEGUNDA', 'SR 6 ANIOS SEGUNDA', 'SR 7 A 9 ANIOS SEGUNDA', 'SR 10 A 12 ANIOS SEGUNDA'
]
cols_13_19 = ['SR 13 A 19 ANIOS PRIMERA', 'SR 13 A 19 ANIOS SEGUNDA', 'SRP 13 A 19 ANIOS PRIMERA', 'SRP 13 A 19 ANIOS SEGUNDA']
cols_20_39 = [
    'SR 20 A 29 ANIOS PRIMERA', 'SR 30 A 39 ANIOS PRIMERA',
    'SR 20 A 29 ANIOS SEGUNDA', 'SR 30 A 39 ANIOS SEGUNDA',
    'SRP 20 A 29 ANIOS PRIMERA', 'SRP 30 A 39 ANIOS PRIMERA',
    'SRP 20 A 29 ANIOS SEGUNDA', 'SRP 30 A 39 ANIOS SEGUNDA'
]
cols_40_49 = [
    'SR 40 A 49 ANIOS PRIMERA', 'SR 40 A 49 ANIOS SEGUNDA',
    'SRP 40 A 49 ANIOS PRIMERA', 'SRP 40 A 49 ANIOS SEGUNDA'
]

def check_sums(name, cols, target):
    print(f"\n--- Category: {name} (Target: {target}) ---")
    current_all = ssa_dur[cols].fillna(0).sum().sum()
    print(f"Total Sum (All dates): {current_all}")
    
    # Check 2026 only
    df_2026 = ssa_dur[pd.to_datetime(ssa_dur['Fecha de registro']) >= '2026-01-01']
    current_2026 = df_2026[cols].fillna(0).sum().sum()
    print(f"Total Sum (2026): {current_2026}")
    
    # Individual columns
    for c in cols:
        if c in df.columns:
            s = ssa_dur[c].fillna(0).sum()
            print(f"  {c}: {s}")

check_sums("6 a 11 meses", cols_6_11m, excel_prev["6 a 11 meses"])
check_sums("1 año", cols_1yr, excel_prev["1 año"])
check_sums("18 meses", cols_18m, excel_prev["18 meses"])
check_sums("Rezagados 2 a 12 años", cols_2_12, excel_prev["Rezagados 2 a 12 años"])
check_sums("13 a 19 años", cols_13_19, excel_prev["13 a 19 años"])
check_sums("20 a 39 años", cols_20_39, excel_prev["20 a 39 años"])
check_sums("40 a 49 años", cols_40_49, excel_prev["40 a 49 años"])
