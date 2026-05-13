import pandas as pd, os, sys

# Paths
workspace = r"C:\\Users\\aicil\\.gemini\\antigravity\\scratch"
output_excel = r"C:\\Users\\aicil\\OneDrive\\Escritorio\\PVU\\SARAMPIÓN\\mezquital\\INFORMES\\Dosis_por_Localidad_y_Edad_Completo_Mezquital_10mayo2026.xlsx"
preview_csv = os.path.join(workspace, "preview_final.xlsx.csv")

try:
    df = pd.read_excel(output_excel)
except Exception as e:
    print('Error loading final Excel:', e)
    sys.exit(1)

# Take first 20 rows
preview = df.head(20)
# Save as CSV
preview.to_csv(preview_csv, index=False)
print('Preview CSV saved to', preview_csv)
