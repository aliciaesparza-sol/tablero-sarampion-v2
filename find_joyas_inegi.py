import pandas as pd

inegi_path = r"C:\Users\aicil\.gemini\antigravity\scratch\iter_durango\iter_10_cpv2020\conjunto_de_datos\conjunto_de_datos_iter_10CSV20.csv"

try:
    df = pd.read_csv(inegi_path, encoding='utf-8')
    # Filter for Mezquital (MUN 14)
    mez = df[df['MUN'] == 14]
    
    # Search for Joyas
    joyas = mez[mez['NOM_LOC'].str.contains('JOYAS', case=False, na=False)]
    print("--- Localities with 'JOYAS' in Mezquital ---")
    print(joyas[['NOM_LOC', 'POBTOT', 'LATITUD', 'LONGITUD']])
    
except Exception as e:
    print(f"Error: {e}")
