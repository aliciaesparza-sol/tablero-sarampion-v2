import pandas as pd

raw_csv = r"C:\Users\aicil\.gemini\antigravity\scratch\mezquital_population_raw.csv"

try:
    df = pd.read_csv(raw_csv, header=None)
    # The "Total" rows are usually at the end of each section or a specific section
    # Let's just sum all ages from the total section if possible, 
    # or just use the sum I have for H+M.
    
    # I already have the extraction logic in extract_full_pop.py
    # Let's run it and get the absolute sum.
    import json
    with open("mezquital_pop_conapo.json", "r") as f:
        pop_data = json.load(f)
        
    # Wait, I only saved the groups. Let's recalculate the absolute total.
except Exception as e:
    print(f"Error: {e}")
