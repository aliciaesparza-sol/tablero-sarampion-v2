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
                out_file.write(df.head(2).to_string() + "\n")
            except Exception as e:
                out_file.write(f"Error parsing sheet: {e}\n")
    except Exception as e:
         out_file.write(f"Error loading file: {e}\n")
    out_file.write("\n\n")

if __name__ == "__main__":
    files = [
        r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\EXISTENCIAS SRP Y SR\EXISTENCIAS_SRP_SR_POR_DIA.xlsx",
        r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\INFORME\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS 10.03.2026.xlsx",
        r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\INFORME\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS 11.03.2026.xlsx",
        r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\INFORME\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS 12.03.2026.xlsx",
        r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\INFORME\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS 13.03.2026.xlsx",
        r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\INFORME\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS 14.03.2026.xlsx"
    ]
    with open("full_dump.txt", "w", encoding="utf-8") as f:
        for filepath in files:
            inspect_file(filepath, f)
