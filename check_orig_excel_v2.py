import pandas as pd

temp_excel = r"C:\Users\aicil\.gemini\antigravity\scratch\orig_temp.xlsx"

try:
    df = pd.read_excel(temp_excel, sheet_name="Concentrado", header=None)
    headers = df.iloc[2].tolist()
    print("Headers in original file:")
    for i, h in enumerate(headers):
        if pd.notna(h):
            print(f"Col {i}: {h}")
            
    # Find AMOLES in column 4
    for i in range(len(df)):
        loc_val = str(df.iloc[i, 4])
        if "AMOLES" in loc_val:
            print(f"\nData for {loc_val} (Row {i}):")
            print(f"Col 34 (TOTAL): {df.iloc[i, 34]}")
            print(f"Col 53 (TOTAL): {df.iloc[i, 53]}")
            print(f"Col 61 (TOTAL): {df.iloc[i, 61]}")
            print(f"Col 78 (TOTAL): {df.iloc[i, 78]}")
            break

except Exception as e:
    print(f"Error: {e}")
