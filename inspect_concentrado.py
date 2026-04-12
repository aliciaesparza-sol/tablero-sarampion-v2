import openpyxl

path = r"c:\Users\aicil\.gemini\antigravity\scratch\temp_conc.xlsx"

try:
    wb = openpyxl.load_workbook(path)
    ws = wb["Concentrado"]
    
    print("--- CONCENTRADO SHEET HEADERS ---")
    # Headers are usually in the first few rows
    for r in range(1, 15):
        row_vals = [str(c.value).strip() if c.value is not None else "None" for c in ws[r]]
        # Filter rows that actually have some text
        if any(v != "None" and len(v) > 0 for v in row_vals):
            print(f"R{r}: {row_vals}")

except Exception as e:
    print(f"Error: {e}")
