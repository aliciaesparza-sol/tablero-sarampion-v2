import pandas as pd
import json

csv_path = r"C:\Descargas_SRP\SRP-SR-2025_04-05-2026 07-59-20.csv"

try:
    df = pd.read_csv(csv_path)
    # Correct municipality name is MEZQUITAL
    mez = df[(df['MUNICIPIO'] == 'MEZQUITAL') & (df['Temporada'] == 2026)]
    
    print(f"Found {len(mez)} rows for MEZQUITAL 2026")
    
    mapping = {
        "1 year": ["SRP 1 ANIO  PRIMERA", "SR 1 ANIO PRIMERA"],
        "2-5 years": ["SRP 2 A 5 ANIOS PRIMERA", "SRP 18 MESES SEGUNDA", "SRP 2 A 5 ANIOS SEGUNDA", "SR 2 A 5 ANIOS PRIMERA", "SR 18 MESES SEGUNDA", "SR 2 A 5 ANIOS SEGUNDA"],
        "6 years": ["SRP 6 ANIOS PRIMERA", "SRP 6 ANIOS SEGUNDA", "SR 6 ANIOS PRIMERA", "SR 6 ANIOS SEGUNDA"],
        "7-9 years": ["SRP 7 A 9 ANIOS PRIMERA", "SRP 7 A 9 ANIOS SEGUNDA", "SR 7 A 9 ANIOS PRIMERA", "SR 7 A 9 ANIOS SEGUNDA"],
        "10-19 years": ["SRP 10 A 19 ANIOS PRIMERA", "SRP 10 A 19 ANIOS SEGUNDA", "SR 10 A 19 ANIOS PRIMERA", "SR 10 A 19 ANIOS SEGUNDA"],
        "20-29 years": ["SRP 20 A 29 ANIOS PRIMERA", "SRP 20 A 29 ANIOS SEGUNDA", "SR 20 A 29 ANIOS PRIMERA", "SR 20 A 29 ANIOS SEGUNDA"],
        "30-39 years": ["SRP 30 A 39 ANIOS PRIMERA", "SRP 30 A 39 ANIOS SEGUNDA", "SR 30 A 39 ANIOS PRIMERA", "SR 30 A 39 ANIOS SEGUNDA"],
        "40-49 years": ["SRP 40 A 49 ANIOS PRIMERA", "SRP 40 A 49 ANIOS SEGUNDA", "SR 40 A 49 ANIOS PRIMERA", "SR 40 A 49 ANIOS SEGUNDA"]
    }
    
    print("--- DOSES BY AGE GROUP (MEZQUITAL 2026) ---")
    results = {}
    for label, cols in mapping.items():
        group_total = 0
        for col in cols:
            if col in mez.columns:
                val = mez[col].sum()
                group_total += int(val)
        results[label] = group_total
        print(f"{label}: {group_total}")
        
    with open("mezquital_doses_age.json", "w") as f:
        json.dump(results, f)

except Exception as e:
    print(f"Error: {e}")
