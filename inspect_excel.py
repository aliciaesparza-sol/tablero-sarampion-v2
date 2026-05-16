import pandas as pd
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')
file_path = Path("temp.xlsx")
try:
    xl = pd.ExcelFile(file_path)
    print("All sheets:", xl.sheet_names)
except Exception as e:
    print(f"Error: {e}")
