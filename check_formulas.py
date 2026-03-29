import openpyxl

filepath = r"C:\Users\aicil\.gemini\antigravity\scratch\CONGRUENCIA_SR_PARA_LLENAR_TEST.xlsx"
wb = openpyxl.load_workbook(filepath, data_only=False)
ws = wb.active

print("Checking rows 2 to 5 for formulas:")
for row in ws.iter_rows(min_row=2, max_row=5):
    for cell in row:
        print(f"{cell.coordinate}: {cell.value}")
