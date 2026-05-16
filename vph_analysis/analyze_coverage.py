# -*- coding: utf-8 -*-
"""
VPH Coverage Analysis Script

This script reads:
- A CSV file with vaccination records (`SRP-SR-2025_05-05-2026 08-53-38.csv`).
- An Excel workbook with population data (`TABLERO_VPH_05-05-2026_3.xlsx`).

It produces a new Excel workbook that contains:
1. Historical coverage per year.
2. Coverage *before* 20 May 2026.
3. Separate coverage for 2025 and 2026.
4. Identification of "susceptible pockets" – jurisdictions where coverage is below 80 %.

The script uses pandas and openpyxl. Adjust column names or thresholds by editing the constants below.
"""

import pathlib
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration – adjust if your source files use different column names
# ---------------------------------------------------------------------------
CSV_PATH = pathlib.Path(r"c:\Descargas_SRP\SRP-SR-2025_05-05-2026 08-53-38.csv")
EXCEL_PATH = pathlib.Path(r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\TABLERO VPH 2025\TABLERO_VPH_05-05-2026_3.xlsx")
# Output configuration – ensure report is saved in the ERRA folder
OUTPUT_DIR = pathlib.Path(r"C:\Users\aicil\.gemini\scratch\ERRA")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = OUTPUT_DIR / "vph_coverage_report.xlsx"

# Expected column names – edit if necessary
# Expected column names – edit if necessary
DATE_COL = "Fecha de registro"          # vaccination date column in CSV (YYYY‑MM‑DD)
JURISDICION_COL = "JURISDICCION"  # area/region identifier in both files
DOSE_COL = "dosis"          # number of doses administered (int)
POP_COL = "poblacion"       # population count for the jurisdiction (int) – in Excel

# Susceptible pocket threshold (coverage % below this value is flagged)
SUSCEPTIBLE_THRESHOLD = 80.0

# ---------------------------------------------------------------------------
def load_csv(csv_path: pathlib.Path) -> pd.DataFrame:
    """Load the vaccination CSV and parse dates."""
    df = pd.read_csv(csv_path, sep=",", encoding="utf-8", dtype={JURISDICION_COL: str})
    # Ensure date column is datetime
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
    return df

def load_excel(excel_path: pathlib.Path) -> pd.DataFrame:
    """Load the population Excel sheet (assumes first sheet contains the data)."""
    df = pd.read_excel(excel_path, dtype={JURISDICION_COL: str})
    return df

def compute_coverage(vac_df: pd.DataFrame, pop_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate coverage percentages per jurisdiction and per year.
    Returns a DataFrame with columns:
        jurisdiccion, year, doses, population, coverage_percent
    """
    # Merge vaccination data with population data on jurisdiction
    merged = vac_df.merge(pop_df[[JURISDICION_COL, POP_COL]], on=JURISDICION_COL, how="left")
    # Extract year from date
    merged["year"] = merged[DATE_COL].dt.year
    # Group by jurisdiction and year
    agg = (
        merged.groupby([JURISDICION_COL, "year"], as_index=False)
        .agg({DOSE_COL: "sum", POP_COL: "first"})
    )
    agg["coverage_percent"] = (agg[DOSE_COL] / agg[POP_COL]) * 100
    return agg

def filter_pre_may20(vac_df: pd.DataFrame) -> pd.DataFrame:
    """Return records dated before 2026‑05‑20."""
    cutoff = datetime(2026, 5, 20)
    return vac_df[vac_df[DATE_COL] < cutoff]

def identify_susceptible_pockets(coverage_df: pd.DataFrame) -> pd.DataFrame:
    """Jurisdictions where coverage < SUSCEPTIBLE_THRESHOLD."""
    return coverage_df[coverage_df["coverage_percent"] < SUSCEPTIBLE_THRESHOLD]

def main():
    vac_df = load_csv(CSV_PATH)
    pop_df = load_excel(EXCEL_PATH)

    # Historical coverage (all years present in CSV)
    hist_cov = compute_coverage(vac_df, pop_df)

    # Coverage before 20 May 2026
    pre_may20_df = filter_pre_may20(vac_df)
    pre_cov = compute_coverage(pre_may20_df, pop_df)

    # Separate coverage for 2025 and 2026
    cov_2025 = hist_cov[hist_cov["year"] == 2025]
    cov_2026 = hist_cov[hist_cov["year"] == 2026]

    # Susceptible pockets (using the most recent year – 2026)
    susceptible = identify_susceptible_pockets(cov_2026)

    # Write results to Excel – each part on its own sheet
    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        hist_cov.to_excel(writer, sheet_name="Historical", index=False)
        pre_cov.to_excel(writer, sheet_name="PreMay20", index=False)
        cov_2025.to_excel(writer, sheet_name="Coverage_2025", index=False)
        cov_2026.to_excel(writer, sheet_name="Coverage_2026", index=False)
        susceptible.to_excel(writer, sheet_name="Susceptible_Pockets", index=False)
    print(f"Report generated: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
