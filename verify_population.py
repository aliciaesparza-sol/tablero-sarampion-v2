import pandas as pd

file_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO SARAMPION V2\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx'

def check_population():
    df = pd.read_excel(file_path, sheet_name='Durango', header=None)
    
    # Durango column index (usually column 5 based on sample)
    durango_col = 5
    mezquital_col = 15
    
    # Headers are at index 3 (Hombres) and 123 (Mujeres)
    h_idx = 4 # Row 5
    m_idx = 124 # Row 125
    
    def get_pop(col_idx):
        pop = {}
        for age in range(101):
            h = float(df.iloc[h_idx + age, col_idx])
            m = float(df.iloc[m_idx + age, col_idx])
            pop[age] = h + m
        return pop

    dur_pop = get_pop(durango_col)
    mez_pop = get_pop(mezquital_col)
    
    print("--- DURANGO CALCULATED METAS ---")
    d_6_11m = dur_pop[0] * 0.5
    d_1y = dur_pop[1] * 1.0
    print(f"6-11m (50% of Age 0): {d_6_11m} (Image says 6335)")
    print(f"1y (100% of Age 1): {d_1y} (Image says 12255)")
    
    print("\n--- MEZQUITAL POPULATION DATA ---")
    m_groups = {
        '6-11m': mez_pop[0] * 0.5,
        '1y': mez_pop[1] * 1.0,
        '18m': mez_pop[1] * 1.0,
        '2-12y': sum(mez_pop[a] for a in range(2, 13)) * 0.5,
        '13-19y': sum(mez_pop[a] for a in range(13, 20)) * 0.5,
        '20-39y': sum(mez_pop[a] for a in range(20, 40)) * 0.5,
        '40-49y': sum(mez_pop[a] for a in range(40, 50)) * 0.5
    }
    for g, v in m_groups.items():
        print(f"Meta {g}: {v}")

check_population()
