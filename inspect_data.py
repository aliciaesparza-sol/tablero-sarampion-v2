import pandas as pd
temp_excel = "temp_excel.xlsx"
df_excel = pd.read_excel(temp_excel, header=7)
for _, row in df_excel.head(3).iterrows():
    print(dict(row))
