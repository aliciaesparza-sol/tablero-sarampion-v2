import pandas as pd

excel_path = r"C:\Users\aicil\.gemini\antigravity\scratch\Formato_Concentrado_Mezquital_2026_Updated.xlsx"

try:
    df = pd.read_excel(excel_path, sheet_name="Concentrado", header=None)
    # Check rows 4-10, columns 4, 78, 82, 83
    print("Sample data from columns 4 (Locality), 78 (Doses?), 82 (Pop), 83 (Reach):")
    print(df.iloc[2:10, [4, 78, 82, 83]])
    
    # Let's also find the column index for "TOTAL" in row 2
    headers = df.iloc[2].tolist()
    total_indices = [i for i, h in enumerate(headers) if h == "TOTAL"]
    print(f"Indices for 'TOTAL': {total_indices}")

except Exception as e:
    print(f"Error: {e}")
