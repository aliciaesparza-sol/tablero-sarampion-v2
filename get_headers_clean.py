import openpyxl

path = r"c:\Users\aicil\.gemini\antigravity\scratch\temp_conc.xlsx"
wb = openpyxl.load_workbook(path)
ws = wb["Concentrado"]

for r in range(1, 4):
    row_vals = [c.value for c in ws[r]]
    print(f"R{r}: {row_vals}")
