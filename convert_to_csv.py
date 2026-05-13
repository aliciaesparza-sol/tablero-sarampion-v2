import pandas as pd, os, sys

# Paths
input_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\INFORMES\Dosis_por_Localidad_y_Edad_Completo_Mezquital_10mayo2026.xlsx"
output_path = r"C:\Users\aicil\.gemini\antigravity\scratch\final_report_preview.csv"

try:
    df = pd.read_excel(input_path, engine='openpyxl')
    df.to_csv(output_path, index=False)
    print(f"CSV saved to {output_path}")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
