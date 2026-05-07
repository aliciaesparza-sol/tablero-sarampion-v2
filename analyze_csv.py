import pandas as pd

csv_path = r"C:\Descargas_SRP\SRP-SR-2025_04-05-2026 07-59-20.csv"

try:
    df = pd.read_csv(csv_path)
    print(f"Columns: {df.columns.tolist()}")
    print(f"Unique values in 'Temporada': {df['Temporada'].unique()}")
    
    # Filter for Mezquital
    mez = df[df['MUNICIPIO'] == 'MEZQUITAL'].copy()
    print(f"Mezquital records: {len(mez)}")
    if len(mez) > 0:
        print(f"Mezquital Temporada unique: {mez['Temporada'].unique()}")
        
except Exception as e:
    print(f"Error: {e}")
