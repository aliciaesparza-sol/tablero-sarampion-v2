import pandas as pd

vph_csv = r"c:\Descargas_VPH\VPH 05-05-2026 05-22-57.csv"

try:
    df = pd.read_csv(vph_csv)
    print("Unique municipalities in VPH file:")
    print(df['MUNICIPIO'].unique())
    
    mez = df[df['MUNICIPIO'] == 'MEZQUITAL']
    print(f"\nRows for Mezquital in VPH: {len(mez)}")
except Exception as e:
    print(f"Error: {e}")
