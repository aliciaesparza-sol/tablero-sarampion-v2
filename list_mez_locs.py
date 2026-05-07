import pandas as pd

inegi_path = r"C:\Users\aicil\.gemini\antigravity\scratch\iter_durango\iter_10_cpv2020\conjunto_de_datos\conjunto_de_datos_iter_10CSV20.csv"

try:
    df = pd.read_csv(inegi_path, encoding='utf-8')
    mez = df[df['MUN'] == 14]
    
    # Large localities
    large = mez[pd.to_numeric(mez['POBTOT'], errors='coerce') > 200]
    print(large[['NOM_LOC', 'POBTOT']].sort_values(by='POBTOT', ascending=False))
    
except Exception as e:
    print(f"Error: {e}")
