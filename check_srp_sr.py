import pandas as pd

temp_excel = r"C:\Users\aicil\.gemini\antigravity\scratch\orig_temp.xlsx"

try:
    df = pd.read_excel(temp_excel, sheet_name="Concentrado", header=None)
    for i in range(len(df)):
        loc_val = str(df.iloc[i, 4])
        if "AMOLES" in loc_val:
            print(f"Data for {loc_val} (Row {i}):")
            print(f"Col 61 (TOTAL VACUNADA): {df.iloc[i, 61]}")
            print(f"Col 62 (SRP APLICADAS): {df.iloc[i, 62]}")
            print(f"Col 63 (SR APLICADAS): {df.iloc[i, 63]}")
            # Total should be SRP + SR?
            break

except Exception as e:
    print(f"Error: {e}")
