import pandas as pd

csv_path = r"C:\Descargas_SRP\SRP-SR-2025_04-05-2026 07-59-20.csv"

try:
    df = pd.read_csv(csv_path)
    # Filter for Mezquital
    mez = df[df['Municipio'] == 'Mezquital']
    print("Doses by age in Mezquital (2026):")
    # Assuming 'Edad' and 'Dosis' (or similar) columns exist. 
    # Let's check columns first.
    print(df.columns.tolist())
    
    # Common columns: 'EDAD', 'DOSIS', 'BIOLOGICO'
    if 'EDAD' in df.columns:
        summary = mez[mez['Temporada'] == 2026].groupby(['EDAD', 'BIOLOGICO']).size().unstack(fill_value=0)
        print(summary)
    else:
        # Try finding age related column
        age_cols = [col for col in df.columns if 'EDAD' in col.upper()]
        print(f"Age columns found: {age_cols}")
        if age_cols:
            summary = mez[mez['Temporada'] == 2026].groupby([age_cols[0], 'BIOLOGICO']).size().unstack(fill_value=0)
            print(summary)

except Exception as e:
    print(f"Error: {e}")
