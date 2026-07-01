import pandas as pd

file_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\POBLACIÓN\POBLACION 2026\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx'

df = pd.read_excel(file_path, sheet_name='Durango')

# Find column index for Mezquital
mezquital_col_idx = None
for idx, val in enumerate(df.iloc[3]):
    if str(val).strip() == 'Mezquital':
        mezquital_col_idx = idx
        break

print(f"Mezquital column index: {mezquital_col_idx}")

if mezquital_col_idx is None:
    print("Could not find Mezquital column!")
    exit(1)

# Now, we split into Hombres and Mujeres
# Hombres is in rows 5 to 114 (based on row 4 = 'Hombres')
hombres_df = df.iloc[5:115].copy()
hombres_df.columns = df.iloc[3]
hombres_df['Edad_parsed'] = df.iloc[5:115, 0].astype(int)
hombres_df['Mezquital_val'] = df.iloc[5:115, mezquital_col_idx].astype(float)

# Mujeres is in rows 123 to 233 (based on row 122 = 'Mujeres')
mujeres_df = df.iloc[123:233].copy()
mujeres_df.columns = df.iloc[3]
mujeres_df['Edad_parsed'] = df.iloc[123:233, 0].astype(int)
mujeres_df['Mezquital_val'] = df.iloc[123:233, mezquital_col_idx].astype(float)

# Under 49 (strictly < 49: ages 0 to 48)
hombres_under_49 = hombres_df[hombres_df['Edad_parsed'] < 49]
mujeres_under_49 = mujeres_df[mujeres_df['Edad_parsed'] < 49]

sum_hombres_u49 = hombres_under_49['Mezquital_val'].sum()
sum_mujeres_u49 = mujeres_under_49['Mezquital_val'].sum()
total_u49 = sum_hombres_u49 + sum_mujeres_u49

print("--- Strictly under 49 years old (Ages 0 to 48) ---")
print(f"Hombres (Ages 0-48): {sum_hombres_u49:,.0f}")
print(f"Mujeres (Ages 0-48): {sum_mujeres_u49:,.0f}")
print(f"Total (Ages 0-48): {total_u49:,.0f}")

# Under or equal to 49 (<= 49: ages 0 to 49)
hombres_lte_49 = hombres_df[hombres_df['Edad_parsed'] <= 49]
mujeres_lte_49 = mujeres_df[mujeres_df['Edad_parsed'] <= 49]

sum_hombres_lte49 = hombres_lte_49['Mezquital_val'].sum()
sum_mujeres_lte49 = mujeres_lte_49['Mezquital_val'].sum()
total_lte49 = sum_hombres_lte49 + sum_mujeres_lte49

print("\n--- 49 years old and under (Ages 0 to 49) ---")
print(f"Hombres (Ages 0-49): {sum_hombres_lte49:,.0f}")
print(f"Mujeres (Ages 0-49): {sum_mujeres_lte49:,.0f}")
print(f"Total (Ages 0-49): {total_lte49:,.0f}")

# Let's print age 49 value separately
h_49 = hombres_df[hombres_df['Edad_parsed'] == 49]['Mezquital_val'].values[0]
m_49 = mujeres_df[mujeres_df['Edad_parsed'] == 49]['Mezquital_val'].values[0]
print(f"\nAge 49 population:")
print(f"Hombres (Age 49): {h_49:,.0f}")
print(f"Mujeres (Age 49): {m_49:,.0f}")
print(f"Total (Age 49): {(h_49 + m_49):,.0f}")
