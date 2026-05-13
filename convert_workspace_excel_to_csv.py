import pandas as pd, os, sys

# Paths in workspace
excel_path = r"C:\\Users\\aicil\\.gemini\\antigravity\\scratch\\final_report.xlsx"
csv_path = r"C:\\Users\\aicil\\.gemini\\antigravity\\scratch\\final_report_workspace.csv"

if not os.path.exists(excel_path):
    print('Excel file not found at', excel_path)
    sys.exit(1)

try:
    df = pd.read_excel(excel_path, engine='openpyxl')
    df.to_csv(csv_path, index=False)
    print('CSV saved to', csv_path)
except Exception as e:
    print('Error:', e)
    sys.exit(1)
