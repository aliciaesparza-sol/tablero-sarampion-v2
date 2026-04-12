import pandas as pd
import openpyxl

path = r"c:\Users\aicil\.gemini\antigravity\scratch\temp_conc.xlsx"

try:
    wb = openpyxl.load_workbook(path)
    ws = wb["Formato bloqueo barrido"]
    
    print("Columns in 'Formato bloqueo barrido':")
    # Read the row that looks like headers (usually around row 2-5)
    for row_idx in range(1, 10):
        row_vals = [cell.value for cell in ws[row_idx]]
        if any(row_vals):
            print(f"Row {row_idx}: {row_vals}")

except Exception as e:
    print(f"Error: {e}")
