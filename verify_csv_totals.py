import pandas as pd

csv_path = r"C:\Descargas_SRP\SRP-SR-2025_04-05-2026 07-59-20.csv"

try:
    df = pd.read_csv(csv_path)
    mez = df[df['MUNICIPIO'] == 'MEZQUITAL']
    
    print(f"Total rows for Mezquital: {len(mez)}")
    
    # Check "Temporada" values
    print("\nRows by Temporada:")
    print(mez['Temporada'].value_counts())
    
    # Calculate totals for 2025 and 2026 combined
    mez_25_26 = mez[mez['Temporada'].isin([2025, 2026])]
    
    srp1 = mez_25_26['SRP  PRIMERA TOTAL'].sum()
    srp2 = mez_25_26['SRP SEGUNDA TOTAL'].sum()
    sr1 = mez_25_26['SR PRIMERA TOTAL'].sum()
    sr2 = mez_25_26['SR SEGUNDA TOTAL'].sum()
    
    total = srp1 + srp2 + sr1 + sr2
    print(f"\nTotals for 2025 + 2026 (using Total Columns):")
    print(f"SRP1: {srp1}")
    print(f"SRP2: {srp2}")
    print(f"SR1: {sr1}")
    print(f"SR2: {sr2}")
    print(f"SUM: {total}")
    
    # Check Institutional breakdown
    ssa = mez_25_26[mez_25_26['INSTITUCION'] == 'SSA']
    imss = mez_25_26[mez_25_26['INSTITUCION'] == 'IMSS-BIENESTAR'] # Check exact name
    print(f"\nInstitutions found: {mez_25_26['INSTITUCION'].unique()}")

except Exception as e:
    print(f"Error: {e}")
