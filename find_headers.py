import pandas as pd

file_path = r"C:\Users\aicil\.gemini\antigravity\scratch\temp_file.xlsx"
sheet_name = "Concentrado"

try:
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    header_row = df.iloc[2].tolist()
    for i, val in enumerate(header_row):
        if pd.notna(val):
            print(f"Column {i}: {val}")

except Exception as e:
    print(f"Error: {e}")
