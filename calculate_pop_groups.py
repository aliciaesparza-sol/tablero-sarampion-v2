import pandas as pd

# File path
raw_csv = r"C:\Users\aicil\.gemini\antigravity\scratch\mezquital_population_raw.csv"

def get_pop_group(df, start_age, end_age, col_idx=15):
    # Ages are in column 0. We need to find where the age column starts with 0 and goes to 100+
    # There are likely multiple sections (Hombres, Mujeres, Total)
    # Let's find the "Total" or "Poblacion Total" section if possible, 
    # otherwise sum Hombres and Mujeres sections.
    
    # Simple approach: Find sections
    hombres_idx = -1
    mujeres_idx = -1
    total_idx = -1
    
    for i, val in enumerate(df.iloc[:, 0].astype(str)):
        if "Hombres" in val: hombres_idx = i
        if "Mujeres" in val: mujeres_idx = i
        if "Total" in val and i > hombres_idx and i > mujeres_idx: total_idx = i
    
    print(f"Indices: H={hombres_idx}, M={mujeres_idx}, T={total_idx}")
    
    # If no Total section found, let's look for the structure
    # Based on the previous view, Hombres starts at row 3 (index 2).
    # Ages 0-100+ follow.
    
    def extract_from_section(start_row):
        section_pop = 0
        for i in range(start_row + 1, start_row + 110):
            if i >= len(df): break
            age_val = str(df.iloc[i, 0])
            if not age_val.replace('.0', '').isdigit(): break
            age = int(float(age_val))
            if start_age <= age <= end_age:
                val = df.iloc[i, col_idx]
                try:
                    section_pop += float(val)
                except:
                    pass
        return section_pop

    if hombres_idx != -1 and mujeres_idx != -1:
        h_pop = extract_from_section(hombres_idx)
        m_pop = extract_from_section(mujeres_idx)
        return h_pop + m_pop
    else:
        # Just use the first section found if others missing
        return extract_from_section(0)

df = pd.read_csv(raw_csv, header=None)

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

print("--- CONAPO Population for Mezquital (2026) ---")
for label, start, end in groups:
    pop = get_pop_group(df, start, end)
    print(f"{label}: {pop}")
