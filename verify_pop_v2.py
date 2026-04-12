import pandas as pd

# Load the population file
pob_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO SARAMPION V2\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx'
df = pd.read_excel(pob_path, sheet_name='Durango', header=None)

# Indices found: Hombres Age 0 at row index 6. Mujeres Age 0 at row index 124.
# Total State column at index 42.
h_start = 6
m_start = 124
total_col = 42

def get_age_totals(col_idx):
    age_pops = {}
    for age in range(101):
        try:
            h = float(df.iloc[h_start + age, col_idx])
            m = float(df.iloc[m_start + age, col_idx])
            age_pops[age] = h + m
        except:
            age_pops[age] = 0
    return age_pops

dur_state = get_age_totals(total_col)

print("--- DURANGO STATE VALIDATION ---")
print(f"Age 0: {dur_state[0]} | 50%: {dur_state[0] * 0.5} (Target 6335?)")
print(f"Age 1: {dur_state[1]} | 100%: {dur_state[1]} (Target 12255?)")
print(f"Ages 2-12 Sum: {sum(dur_state[a] for a in range(2, 13))} | 50%: {sum(dur_state[a] for a in range(2, 13)) * 0.5} (Target 38054?)")

# MEZQUITAL (Col 15)
mez_pop = get_age_totals(15)
print("\n--- MEZQUITAL POPULATION ENTIRE ---")
print(f"Age 0: {mez_pop[0]}")
print(f"Age 1: {mez_pop[1]}")
print(f"Ages 2-12 Sum: {sum(mez_pop[a] for a in range(2, 13))}")
