import pandas as pd

file1 = r"C:\Users\aicil\.gemini\antigravity\scratch\VPH25-26_TOP100PTES_copy.xlsx"

print("Columns in TOP100PTES copy:")
try:
    df1 = pd.read_excel(file1)
    print(df1.columns.tolist())
except Exception as e:
    print("Error reading file1:", e)
