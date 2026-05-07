import pandas as pd

file_path = r"C:\Users\aicil\.gemini\antigravity\scratch\temp_file.xlsx"
sheet_name = "Concentrado"

try:
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    # Localities are in column 4, starting from row 3 or 4
    localities = df.iloc[3:, 4].dropna().unique().tolist()
    print(f"Unique localities in file ({len(localities)}):")
    for loc in sorted(localities):
        print(f"- {loc}")

except Exception as e:
    print(f"Error: {e}")
