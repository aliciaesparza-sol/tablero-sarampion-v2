import pandas as pd

csv_path = r"C:\Descargas_SRP\SRP-SR-2025_04-05-2026 07-59-20.csv"

try:
    df = pd.read_csv(csv_path)
    mez = df[(df['MUNICIPIO'] == 'MEZQUITAL') & (df['Temporada'].isin([2025, 2026]))]
    
    # List all columns that start with SRP or SR
    all_cols = [c for c in mez.columns if (c.startswith('SRP') or c.startswith('SR')) and 'TOTAL' not in c]
    
    # Columns already in mapping
    mapping_cols = []
    # (Extract from mapping defined before)
    
    # Just calculate sum of all "non-total" columns
    print("Sum of individual columns:")
    total_sum = 0
    for c in all_cols:
        s = mez[c].sum()
        if s > 0:
            print(f"{c}: {s}")
            total_sum += s
    print(f"\nTotal sum of individual columns: {total_sum}")
    
    # Compare with "Total" columns sum
    srp1 = mez['SRP  PRIMERA TOTAL'].sum()
    srp2 = mez['SRP SEGUNDA TOTAL'].sum()
    sr1 = mez['SR PRIMERA TOTAL'].sum()
    sr2 = mez['SR SEGUNDA TOTAL'].sum()
    print(f"Total from summary columns: {srp1 + srp2 + sr1 + sr2}")

except Exception as e:
    print(f"Error: {e}")
