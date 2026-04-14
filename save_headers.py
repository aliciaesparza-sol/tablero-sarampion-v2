import openpyxl
import json

path = r"c:\Users\aicil\.gemini\antigravity\scratch\temp_conc.xlsx"
wb = openpyxl.load_workbook(path)
ws = wb["Concentrado"]

headers = {}
for r in range(1, 10):
    headers[f"Row_{r}"] = [str(c.value) for c in ws[r]]

with open(r"c:\Users\aicil\.gemini\antigravity\scratch\headers.json", "w") as f:
    json.dump(headers, f, indent=2)
print("Headers saved to headers.json")
