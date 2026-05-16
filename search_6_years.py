import pandas as pd
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')
file_path = Path("temp.xlsx")

try:
    xl = pd.ExcelFile(file_path)
    for sheet in xl.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet, header=None)
        mask = df.map(lambda x: '6 años' in str(x).lower() or '6 años' in str(x).lower() if pd.notnull(x) else False)
        count = mask.sum().sum()
        if count > 0:
            print(f"Sheet '{sheet}': Found {count} occurrences.")
            # Print where it was found
            row_indices, col_indices = mask.values.nonzero()
            for r, c in zip(row_indices[:5], col_indices[:5]):
                print(f"  Row {r}, Col {c}: {df.iloc[r, c]}")
except Exception as e:
    print(f"Error: {e}")
