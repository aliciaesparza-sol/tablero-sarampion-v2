import pandas as pd
with open("cols_611.txt", "w", encoding="utf-8") as f:
    df = pd.read_excel('temp_excel2.xlsx', sheet_name='🍼 6-11 Meses', header=6)
    f.write(str(df.columns.tolist()[:15]) + "\n")
    for _, row in df.head(3).iterrows():
        f.write(str(dict(row)) + "\n")
