import pandas as pd

file_path = r"C:\Users\aicil\.gemini\antigravity\scratch\temp_file.xlsx"
sheet_name = "Concentrado"

try:
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    print("First 10 rows and first 10 columns:")
    print(df.iloc[:10, :20])

except Exception as e:
    print(f"Error: {e}")
