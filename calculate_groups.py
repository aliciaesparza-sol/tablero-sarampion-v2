import pandas as pd

file_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\POBLACIÓN\POBLACION 2026\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx'
df = pd.read_excel(file_path, sheet_name='Durango')

# Find column index for Mezquital
mezquital_col_idx = None
for idx, val in enumerate(df.iloc[3]):
    if str(val).strip() == 'Mezquital':
        mezquital_col_idx = idx
        break

if mezquital_col_idx is None:
    print("Could not find Mezquital column!")
    exit(1)

# Extract Hombres and Mujeres datasets
hombres_df = df.iloc[5:115].copy()
hombres_df['Edad'] = df.iloc[5:115, 0].astype(int)
hombres_df['Hombres'] = df.iloc[5:115, mezquital_col_idx].astype(int)

mujeres_df = df.iloc[123:233].copy()
mujeres_df['Edad'] = df.iloc[123:233, 0].astype(int)
mujeres_df['Mujeres'] = df.iloc[123:233, mezquital_col_idx].astype(int)

# Merge on Edad
merged = pd.merge(hombres_df[['Edad', 'Hombres']], mujeres_df[['Edad', 'Mujeres']], on='Edad')
merged['Total'] = merged['Hombres'] + merged['Mujeres']

# Full age-by-age dict
pop_h = {row['Edad']: row['Hombres'] for _, row in merged.iterrows()}
pop_m = {row['Edad']: row['Mujeres'] for _, row in merged.iterrows()}
pop_t = {row['Edad']: row['Total'] for _, row in merged.iterrows()}

# We also need total population of Mezquital (which is the sum over all ages 0 to 109)
# Let's read from the spreadsheet or sum all rows 5-114 and 123-232
tot_hombres = df.iloc[5:115, mezquital_col_idx].astype(int).sum()
tot_mujeres = df.iloc[123:233, mezquital_col_idx].astype(int).sum()
grand_total = tot_hombres + tot_mujeres

# Under 49 (0 to 49 years old)
sum_h_0_49 = merged[merged['Edad'] <= 49]['Hombres'].sum()
sum_m_0_49 = merged[merged['Edad'] <= 49]['Mujeres'].sum()
sum_t_0_49 = merged[merged['Edad'] <= 49]['Total'].sum()

print("Mezquital Grand Total:", grand_total)
print("Mezquital 0-49 Total:", sum_t_0_49)

# Group calculations (Universo and Meta)
# Group: 6-11 meses
# Universo: Age 0
# Meta: 50% of Age 0
u_6_11m_h = pop_h[0]
u_6_11m_m = pop_m[0]
u_6_11m_t = pop_t[0]
m_6_11m_h = round(u_6_11m_h * 0.5)
m_6_11m_m = round(u_6_11m_m * 0.5)
m_6_11m_t = round(u_6_11m_t * 0.5)

# Group: 1 año
# Universo: Age 1
# Meta: 100% of Age 1
u_1y_h = pop_h[1]
u_1y_m = pop_m[1]
u_1y_t = pop_t[1]
m_1y_h = u_1y_h
m_1y_m = u_1y_m
m_1y_t = u_1y_t

# Group: 18 meses
# Universo: Age 1
# Meta: 100% of Age 1
u_18m_h = pop_h[1]
u_18m_m = pop_m[1]
u_18m_t = pop_t[1]
m_18m_h = u_18m_h
m_18m_m = u_18m_m
m_18m_t = u_18m_t

# Group: 6 años
# Universo: Age 6
# Meta: 100% of Age 6
u_6y_h = pop_h[6]
u_6y_m = pop_m[6]
u_6y_t = pop_t[6]
m_6y_h = u_6y_h
m_6y_m = u_6y_m
m_6y_t = u_6y_t

# Group: 2 a 12 años
# Universo: Ages 2 to 12
# Meta: 50% of Ages 2 to 12
u_2_12y_h = sum(pop_h[a] for a in range(2, 13))
u_2_12y_m = sum(pop_m[a] for a in range(2, 13))
u_2_12y_t = sum(pop_t[a] for a in range(2, 13))
m_2_12y_h = round(u_2_12y_h * 0.5)
m_2_12y_m = round(u_2_12y_m * 0.5)
m_2_12y_t = round(u_2_12y_t * 0.5)

# Group: 13 a 19 años
# Universo: Ages 13 to 19
# Meta: 50% of Ages 13 to 19
u_13_19y_h = sum(pop_h[a] for a in range(13, 20))
u_13_19y_m = sum(pop_m[a] for a in range(13, 20))
u_13_19y_t = sum(pop_t[a] for a in range(13, 20))
m_13_19y_h = round(u_13_19y_h * 0.5)
m_13_19y_m = round(u_13_19y_m * 0.5)
m_13_19y_t = round(u_13_19y_t * 0.5)

# Group: 20 a 39 años
# Universo: Ages 20 to 39
# Meta: 50% of Ages 20 to 39
u_20_39y_h = sum(pop_h[a] for a in range(20, 40))
u_20_39y_m = sum(pop_m[a] for a in range(20, 40))
u_20_39y_t = sum(pop_t[a] for a in range(20, 40))
m_20_39y_h = round(u_20_39y_h * 0.5)
m_20_39y_m = round(u_20_39y_m * 0.5)
m_20_39y_t = round(u_20_39y_t * 0.5)

# Group: 40 a 49 años
# Universo: Ages 40 to 49
# Meta: 50% of Ages 40 to 49
u_40_49y_h = sum(pop_h[a] for a in range(40, 50))
u_40_49y_m = sum(pop_m[a] for a in range(40, 50))
u_40_49y_t = sum(pop_t[a] for a in range(40, 50))
m_40_49y_h = round(u_40_49y_h * 0.5)
m_40_49y_m = round(u_40_49y_m * 0.5)
m_40_49y_t = round(u_40_49y_t * 0.5)

print("\n--- RESULTS TABLE DATA ---")
print(f"6-11m H={u_6_11m_h}/{m_6_11m_h}, M={u_6_11m_m}/{m_6_11m_m}, T={u_6_11m_t}/{m_6_11m_t}")
print(f"1y H={u_1y_h}/{m_1y_h}, M={u_1y_m}/{m_1y_m}, T={u_1y_t}/{m_1y_t}")
print(f"18m H={u_18m_h}/{m_18m_h}, M={u_18m_m}/{m_18m_m}, T={u_18m_t}/{m_18m_t}")
print(f"6y H={u_6y_h}/{m_6y_h}, M={u_6y_m}/{m_6y_m}, T={u_6y_t}/{m_6y_t}")
print(f"2-12y H={u_2_12y_h}/{m_2_12y_h}, M={u_2_12y_m}/{m_2_12y_m}, T={u_2_12y_t}/{m_2_12y_t}")
print(f"13-19y H={u_13_19y_h}/{m_13_19y_h}, M={u_13_19y_m}/{m_13_19y_m}, T={u_13_19y_t}/{m_13_19y_t}")
print(f"20-39y H={u_20_39y_h}/{m_20_39y_h}, M={u_20_39y_m}/{m_20_39y_m}, T={u_20_39y_t}/{m_20_39y_t}")
print(f"40-49y H={u_40_49y_h}/{m_40_49y_h}, M={u_40_49y_m}/{m_40_49y_m}, T={u_40_49y_t}/{m_40_49y_t}")
