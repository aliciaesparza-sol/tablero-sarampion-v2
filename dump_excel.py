import openpyxl
import pandas as pd
import json

wb = openpyxl.load_workbook(r'c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\TABLERO VPH 2025\TABLERO_VPH_05-05-2026_3.xlsx', data_only=True)
ws = wb['AVANCE AL 05-MAY-2026']

data = []
for row in ws.iter_rows(min_row=1, max_row=40, min_col=1, max_col=15):
    row_data = []
    for cell in row:
        row_data.append(str(cell.value) if cell.value is not None else '')
    data.append(row_data)

with open('out.txt', 'w', encoding='utf-8') as f:
    for row in data:
        f.write('\t'.join(row) + '\n')

print("Done")
