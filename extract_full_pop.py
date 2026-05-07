import pandas as pd

excel_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\POBLACIÓN\POBLACION 2026\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx"

try:
    df = pd.read_excel(excel_path, sheet_name='Durango', header=None)
    
    # Mezquital is column 15 (based on previous analysis)
    # Let's confirm column 15 is Mezquital by looking at row 4 (index 4)
    municipality = str(df.iloc[4, 15])
    print(f"Column 15 is: {municipality}")
    
    col_idx = 15
    
    # Find sections
    hombres_idx = -1
    mujeres_idx = -1
    
    for i in range(len(df)):
        val = str(df.iloc[i, 0])
        if "Hombres" in val:
            hombres_idx = i
        elif "Mujeres" in val:
            mujeres_idx = i
            
    print(f"Hombres at {hombres_idx}, Mujeres at {mujeres_idx}")
    
    def get_ages(start_idx):
        data = {}
        for i in range(start_idx + 1, len(df)):
            age_val = str(df.iloc[i, 0])
            try:
                age = int(float(age_val))
                pop = float(df.iloc[i, col_idx])
                data[age] = pop
            except:
                if len(data) > 50: break
                continue
        return data

    h_pop = get_ages(hombres_idx)
    m_pop = get_ages(mujeres_idx)
    
    total_pop = {}
    for age in range(110): # 0 to 109
        total_pop[age] = h_pop.get(age, 0) + m_pop.get(age, 0)
        
    groups = [
        ("1 year", 1, 1),
        ("2-5 years", 2, 5),
        ("6 years", 6, 6),
        ("7-9 years", 7, 9),
        ("10-19 years", 10, 19),
        ("20-29 years", 20, 29),
        ("30-39 years", 30, 39),
        ("40-49 years", 40, 49)
    ]

    print("\n--- MEZQUITAL TOTAL POPULATION (CONAPO 2026) ---")
    results = {}
    for label, start, end in groups:
        pop = sum(total_pop.get(a, 0) for a in range(start, end + 1))
        results[label] = pop
        print(f"{label}: {pop}")
    
    # Save results to a json for later use
    import json
    with open("mezquital_pop_conapo.json", "w") as f:
        json.dump(results, f)

except Exception as e:
    print(f"Error: {e}")
