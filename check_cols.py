import pandas as pd
import string

path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\VPH25-26_TOP100PTES.xlsx"
df = pd.read_excel(path)

def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num - 1 # 0-indexed

def num2col(num):
    col = ""
    num += 1
    while num > 0:
        num, remainder = divmod(num - 1, 26)
        col = chr(65 + remainder) + col
    return col

print("Columns:")
for i, c in enumerate(df.columns):
    print(f"{num2col(i)} ({i}): {c}")
