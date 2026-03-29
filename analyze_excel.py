import pandas as pd
import json

file_path = r'C:/Users/aicil/.gemini/antigravity/scratch/temp_data.xlsx'
xl = pd.ExcelFile(file_path)

all_data = {}

for name in xl.sheet_names:
    df = pd.read_excel(xl, sheet_name=name, header=None)
    # Find the header row (contains 'Municipio' usually)
    header_row = -1
    for i in range(len(df)):
        row_values = [str(x) for x in df.iloc[i].tolist()]
        if 'Municipio' in row_values:
            header_row = i
            break
    
    if header_row != -1:
        columns = [str(x).replace('\n', ' ') for x in df.iloc[header_row].tolist()]
        # sample some data
        sample = df.iloc[header_row+1:header_row+4].values.tolist()
        all_data[name] = {
            'columns': columns,
            'header_row': header_row,
            'sample': sample
        }

with open(r'C:/Users/aicil/.gemini/antigravity/scratch/sheet_info.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print("Analysis complete. Saved to sheet_info.json")
