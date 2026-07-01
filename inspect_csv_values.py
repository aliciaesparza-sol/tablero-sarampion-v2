import pandas as pd
import os
from io import StringIO

BASE_DIR = r"C:\Users\aicil\.gemini\antigravity-ide\scratch"
csv_path = os.path.join(BASE_DIR, "SRP-SR-2025_02-04-2026 10-40-30.csv")

if not os.path.exists(csv_path):
    print("CSV not found:", csv_path)
    exit(1)

with open(csv_path, 'r', encoding='latin1') as f:
    content = f.read()

lines = content.split("\n")
fixed = []
for line in lines:
    line = line.strip()
    if line.startswith('"') and line.endswith('"'):
        line = line[1:-1].replace('""', '"')
    fixed.append(line)

df = pd.read_csv(StringIO("\n".join(fixed)), encoding='latin1', low_memory=False)
df.columns = df.columns.str.strip()

print("\nUNIQUE INSTITUTIONS:")
print(df["INSTITUCION"].unique())

print("\nUNIQUE JURISDICTIONS FOR DURANGO:")
print(df[df["ESTADO"] == "DURANGO"]["JURISDICCION"].unique())

print("\nFECHA DE REGISTRO MIN/MAX:")
df["Fecha de registro"] = pd.to_datetime(df["Fecha de registro"], errors="coerce")
print("Min:", df["Fecha de registro"].min())
print("Max:", df["Fecha de registro"].max())
