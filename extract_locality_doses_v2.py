import pandas as pd
import json

excel_path = r"C:\Users\aicil\.gemini\antigravity\scratch\Formato_Concentrado_Mezquital_2026_Updated.xlsx"

try:
    df = pd.read_excel(excel_path, sheet_name="Concentrado", header=None)
    # Localities start at row 4 (index 3). Data from row 5 (index 4).
    # Col 4: Localidad, Col 61: TOTAL (Correct doses col), Col 82: Poblacion, Col 83: Alcance
    
    rows = []
    for i in range(4, len(df)):
        loc = df.iloc[i, 4]
        doses = df.iloc[i, 61]
        pop = df.iloc[i, 82]
        reach = df.iloc[i, 83]
        
        if pd.notna(loc) and str(loc).strip() != "":
            rows.append({
                "Localidad": str(loc).strip(),
                "Doses": doses if pd.notna(doses) else 0,
                "Population": pop if pd.notna(pop) else 0,
                "Reach": reach if pd.notna(reach) else 0
            })
            
    # Sort by Doses
    rows.sort(key=lambda x: x['Doses'], reverse=True)
    
    with open("locality_doses_v2.json", "w") as f:
        json.dump(rows, f)
    print(f"Extracted {len(rows)} localities.")

except Exception as e:
    print(f"Error: {e}")
