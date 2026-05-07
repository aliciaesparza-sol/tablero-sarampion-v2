import pandas as pd

inegi_path = r"C:\Users\aicil\.gemini\antigravity\scratch\iter_durango\iter_10_cpv2020\conjunto_de_datos\conjunto_de_datos_iter_10CSV20.csv"

try:
    df = pd.read_csv(inegi_path, encoding='utf-8')
    mez = df[df['MUN'] == 14]
    
    # Search for OCOTAN, BAJIO, MANUEL, CARBONERAS
    targets = ["OCOTAN", "BAJIO", "MANUEL", "CARBONERAS", "JOYAS"]
    for t in targets:
        match = mez[mez['NOM_LOC'].str.contains(t, case=False, na=False)]
        print(f"\n--- Matches for {t} ---")
        print(match[['NOM_LOC', 'POBTOT']])
        
except Exception as e:
    print(f"Error: {e}")
