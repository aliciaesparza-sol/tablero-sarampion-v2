import pandas as pd

inegi_path = r"C:\Users\aicil\.gemini\antigravity\scratch\iter_durango\iter_10_cpv2020\conjunto_de_datos\conjunto_de_datos_iter_10CSV20.csv"

try:
    df = pd.read_csv(inegi_path, encoding='utf-8')
    mez = df[df['MUN'] == 14]
    joyas = mez[mez['NOM_LOC'].str.fullmatch('Las Joyas', case=False, na=False)]
    print(f"Total population for 'Las Joyas' in Mezquital: {pd.to_numeric(joyas['POBTOT'], errors='coerce').sum()}")
    
except Exception as e:
    print(f"Error: {e}")
