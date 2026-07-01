import pandas as pd
import os

# Paths
excel_path = r"C:/Users/aicil/OneDrive/Escritorio/PVU/ANEXOS DGO/VACUNACIÓN ANEXOS FINAL.xlsx"
csv_path = r"C:/Users/aicil/OneDrive/Escritorio/PVU/ANEXOS DGO/Anexos_Durango.csv"
output_csv = r"C:/Users/aicil/.gemini/antigravity-ide/scratch/vaccination_summary.csv"
report_path = r"C:/Users/aicil/.gemini/antigravity-ide/scratch/vaccination_report.txt"

# Read files
try:
    df_excel = pd.read_excel(excel_path)
except Exception as e:
    raise RuntimeError(f"Error reading Excel file: {e}")

try:
    df_csv = pd.read_csv(csv_path, delimiter=';')
except Exception as e:
    raise RuntimeError(f"Error reading CSV file: {e}")

# Assuming the Excel has columns: 'Centro', 'Biologico', 'Dosis'
# If column names differ, rename generically for processing
expected_cols = {'Centro', 'Biologico', 'Dosis'}
if not expected_cols.issubset(set(df_excel.columns)):
    # Try to infer columns by position: first column centre code, second biologic, third dose count
    df_excel = df_excel.rename(columns={df_excel.columns[0]: 'Centro', df_excel.columns[1]: 'Biologico', df_excel.columns[2]: 'Dosis'})

# Merge with CSV to get center details (using 'num' from CSV as center code)
merged = pd.merge(df_excel, df_csv, left_on='Centro', right_on='num', how='left')

# Group by center and biologic to sum doses
summary = merged.groupby(['Centro', 'Biologico']).agg({'Dosis': 'sum'}).reset_index()
# Total doses per center
total_per_center = merged.groupby('Centro').agg({'Dosis': 'sum'}).reset_index().rename(columns={'Dosis': 'TotalDosis'})
summary = summary.merge(total_per_center, on='Centro')

# Save summary CSV
summary.to_csv(output_csv, index=False, sep=';')

# Create executive report in Spanish
report_lines = []
report_lines.append("Informe Ejecutivo de Vacunación en Centros de Rehabilitación – Durango\n")
report_lines.append("Resumen por centro y biológico:\n")
for _, row in summary.iterrows():
    report_lines.append(f"Centro {row['Centro']}: {row['Biologico']} – Dosis aplicadas: {row['Dosis']} (Total centro: {row['TotalDosis']})")
report_lines.append("\nTotal de dosis aplicadas en todos los centros: " + str(merged['Dosis'].sum()))

with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print('Summary CSV generated at:', output_csv)
print('Executive report generated at:', report_path)
