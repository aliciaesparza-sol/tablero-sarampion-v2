import pandas as pd

# Load the population file
pob_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO SARAMPION V2\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx'
df = pd.read_excel(pob_path, sheet_name='Durango', header=None)

# Municipality names are in Row 2 (index 1)
mun_row = df.iloc[1]
print("--- Municipality Map ---")
for i, val in enumerate(mun_row):
    if pd.notna(val):
        print(f"Col {i}: {val}")

# Age zero is in Row 4 (index 3) or Row 5 (index 4)?
# The sample showed Row 4 (index 3) is "Hombres"
# Row 5 (index 4) is Age 0.
print("\n--- Rows Inspection ---")
for i in range(10):
    print(f"Row {i}: {df.iloc[i, 0:6].tolist()}")

# Finding 'Mujeres' block
m_row_idx = df[df[0].astype(str).str.contains('Mujeres', na=False)].index[0]
print(f"Mujeres starts at row index: {m_row_idx}")

def get_age_totals(col_idx):
    # Sum Hombres and Mujeres for each age 0-100
    h_start = 4 # Row 5
    m_start = m_row_idx + 1 # Row after 'Mujeres' label
    age_pops = {}
    for age in range(101):
        h = float(df.iloc[h_start + age, col_idx])
        m = float(df.iloc[m_start + age, col_idx])
        age_pops[age] = h + m
    return age_pops

# Check column for Durango (Total State?)
# Usually there is a column for the whole state or I sum all municipalities.
# Let's find 'Poblacion Total H y M' column
total_col_idx = [i for i, val in enumerate(mun_row) if 'Poblacion Total' in str(val)][0]
print(f"Total Population Column index: {total_col_idx}")

dur_state_pop = get_age_totals(total_col_idx)
mez_pop = get_age_totals(15) # Mezquital was 15

print("\n--- Durango State Verification ---")
print(f"Age 0: {dur_state_pop[0]} | 50%: {dur_state_pop[0] * 0.5} (Target 6335?)")
print(f"Age 1: {dur_state_pop[1]} | 100%: {dur_state_pop[1]} (Target 12255?)")

print("\n--- Mezquital Targets ---")
print(f"Age 0: {mez_pop[0]} | 6-11m Meta: {mez_pop[0] * 0.5}")
print(f"Age 1: {mez_pop[1]} | 1y Meta: {mez_pop[1]}")
