import pandas as pd
import sys

filepath = r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\REPORTE_SRP-SR-CENSIA\SRP-SR-2025_14-03-2026 06-41-16.csv'
df = pd.read_csv(filepath, nrows=5)
with open('csv_columns.txt', 'w', encoding='utf-8') as f:
    f.write("Columns: " + str(list(df.columns)) + "\n")
    f.write("Unique vaccines (if any): " + str(list(set(df['Vacuna Aplicada'].values))) if 'Vacuna Aplicada' in df.columns else "No 'Vacuna Aplicada' column\n")
    for col in df.columns:
        if 'vac' in col.lower() or 'bio' in col.lower():
            f.write(f"Vaccine column candidate: {col}\n")
