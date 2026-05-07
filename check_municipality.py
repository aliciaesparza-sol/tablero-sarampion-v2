import pandas as pd

csv_path = r"C:\Descargas_SRP\SRP-SR-2025_04-05-2026 07-59-20.csv"

try:
    df = pd.read_csv(csv_path)
    print("Unique municipalities:")
    print(df['MUNICIPIO'].unique())
    
    # Check Mezquital specifically
    mez_rows = df[df['MUNICIPIO'].astype(str).str.contains('Mezquital', case=False)]
    print(f"\nFound {len(mez_rows)} rows for Mezquital")
    if not mez_rows.empty:
        print(f"Exact name: '{mez_rows['MUNICIPIO'].iloc[0]}'")
        
except Exception as e:
    print(f"Error: {e}")
