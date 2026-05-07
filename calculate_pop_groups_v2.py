import pandas as pd

raw_csv = r"C:\Users\aicil\.gemini\antigravity\scratch\mezquital_population_raw.csv"

try:
    df = pd.read_csv(raw_csv, header=None)
    
    # Clean the dataframe: remove any rows that are all NaN
    df = df.dropna(how='all')
    
    # Mezquital is column 15
    col_idx = 15
    
    # Identify indices of sections
    hombres_idx = -1
    mujeres_idx = -1
    total_idx = -1
    
    for i in range(len(df)):
        val = str(df.iloc[i, 0])
        if "Hombres" in val: hombres_idx = i
        if "Mujeres" in val: mujeres_idx = i
        if "Total" in val and i > 5: total_idx = i # Skip header Total
    
    print(f"Sections found at: H={hombres_idx}, M={mujeres_idx}, T={total_idx}")
    
    def extract_ages(start_idx):
        ages = {}
        for i in range(start_idx + 1, len(df)):
            age_val = str(df.iloc[i, 0])
            # Check if it's a numeric age
            try:
                age = int(float(age_val))
                pop_val = df.iloc[i, col_idx]
                pop = float(pop_val)
                ages[age] = pop
            except:
                # If we hit a non-numeric row, the section might be over
                if len(ages) > 50: # Assume a section has many ages
                    break
                continue
        return ages

    h_ages = extract_ages(hombres_idx) if hombres_idx != -1 else {}
    m_ages = extract_ages(mujeres_idx) if mujeres_idx != -1 else {}
    
    print(f"Extracted {len(h_ages)} ages for Hombres and {len(m_ages)} for Mujeres")
    
    # Sum them
    total_ages = {}
    all_keys = set(h_ages.keys()).union(set(m_ages.keys()))
    for age in all_keys:
        total_ages[age] = h_ages.get(age, 0) + m_ages.get(age, 0)
        
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

    print("\n--- RESULTS ---")
    for label, start, end in groups:
        sum_pop = sum(total_ages.get(a, 0) for a in range(start, end + 1))
        print(f"{label}: {sum_pop}")

except Exception as e:
    print(f"Error: {e}")
