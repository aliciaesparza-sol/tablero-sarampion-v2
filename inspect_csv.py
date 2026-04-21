import pandas as pd

df = pd.read_csv(r"c:\Descargas_SRP\SRP-SR-2025_20-04-2026 03-35-04.csv", nrows=1)
cols = df.columns.tolist()
for i, col in enumerate(cols):
    print(f"{i}: {col}")
