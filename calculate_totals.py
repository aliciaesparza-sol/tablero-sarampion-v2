import pandas as pd

csv_path = r"C:\Descargas_SRP\SRP-SR-2025_04-05-2026 07-59-20.csv"

def get_totals(df_year):
    # Map institutions
    # SSA is SSA
    # IMSS BIENESTAR is usually IMSS-OP or similar. Let's check unique values.
    
    # Actually, let's just group by INSTITUCION
    # SRP PRIMERA TOTAL -> 'SRP  PRIMERA TOTAL'
    # SRP SEGUNDA TOTAL -> 'SRP SEGUNDA TOTAL'
    # SR PRIMERA TOTAL -> 'SR PRIMERA TOTAL'
    # SR SEGUNDA TOTAL -> 'SR SEGUNDA TOTAL'
    
    cols = ['SRP  PRIMERA TOTAL', 'SRP SEGUNDA TOTAL', 'SR PRIMERA TOTAL', 'SR SEGUNDA TOTAL']
    summary = df_year.groupby('INSTITUCION')[cols].sum()
    summary['TOTAL'] = summary.sum(axis=1)
    
    # Add column Total
    summary.loc['Suma total'] = summary.sum()
    
    return summary

try:
    df = pd.read_csv(csv_path)
    mez = df[df['MUNICIPIO'] == 'MEZQUITAL'].copy()
    
    print("--- 2025 MEZQUITAL ---")
    summary_2025 = get_totals(mez[mez['Temporada'] == 2025])
    print(summary_2025)
    
    print("\n--- 2026 MEZQUITAL FULL ---")
    summary_2026 = get_totals(mez[mez['Temporada'] == 2026])
    print(summary_2026.to_string())

except Exception as e:
    print(f"Error: {e}")
