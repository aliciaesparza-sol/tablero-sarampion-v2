import pandas as pd
import sys

def inspect_file(filepath, out_file):
    out_file.write(f"=== File: {filepath} ===\n")
    try:
        xl = pd.ExcelFile(filepath)
        out_file.write(f"Sheet names: {xl.sheet_names}\n")
        for sheet in xl.sheet_names:
            out_file.write(f"\n--- Sheet: {sheet} ---\n")
            try:
                df = xl.parse(sheet, nrows=2)
                out_file.write(f"Columns: {list(df.columns)}\n")
            except Exception as e:
                out_file.write(f"Error parsing sheet: {e}\n")
    except Exception as e:
         out_file.write(f"Error loading file: {e}\n")
    out_file.write("\n\n")

if __name__ == "__main__":
    filepath = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\REPORTE_SRP-SR-CENSIA\10. DURANGO.xlsx"
    with open("durango_dump_cols.txt", "w", encoding="utf-8") as f:
        inspect_file(filepath, f)
