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
                df = xl.parse(sheet, nrows=5)
                out_file.write(f"Columns: {list(df.columns)}\n")
                out_file.write(df.head(5).to_string() + "\n")
            except Exception as e:
                out_file.write(f"Error parsing sheet: {e}\n")
    except Exception as e:
         out_file.write(f"Error loading file: {e}\n")
    out_file.write("\n\n")

if __name__ == "__main__":
    files = [
        r"C:\Users\aicil\.gemini\antigravity\scratch\CONGRUENCIA_SR_PARA_LLENAR_TEST.xlsx",
        r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\EXISTENCIAS SRP Y SR\EXISTENCIAS_DE_INSTITUCIONES_SRP_Y_SR.xlsx"
    ]
    with open("congruencia_dump.txt", "w", encoding="utf-8") as f:
        for filepath in files:
            inspect_file(filepath, f)
