import pandas as pd
csv_path = r"C:\Descargas_SRP\SRP-SR-2025_04-05-2026 07-59-20.csv"
df = pd.read_csv(csv_path, nrows=0)
print(df.columns.tolist())
