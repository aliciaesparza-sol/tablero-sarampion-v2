import pandas as pd

temp_excel = r"C:\Users\aicil\.gemini\antigravity\scratch\orig_temp.xlsx"

try:
    df = pd.read_excel(temp_excel, sheet_name="Concentrado", header=None)
    headers = df.iloc[2].tolist()
    
    # Target columns
    col_loc = 4
    col_age_start = 54
    col_age_end = 61 # TOTAL
    
    age_groups = [headers[i] for i in range(col_age_start, col_age_end + 1)]
    
    # Process data
    loc_data = {}
    for i in range(4, len(df)):
        loc = str(df.iloc[i, col_loc]).strip().upper()
        if loc == "NAN" or loc == "": continue
        
        # Get age values
        vals = []
        for j in range(col_age_start, col_age_end + 1):
            v = pd.to_numeric(df.iloc[i, j], errors='coerce')
            vals.append(v if not pd.isna(v) else 0)
            
        if loc not in loc_data:
            loc_data[loc] = [0] * len(vals)
            
        for k in range(len(vals)):
            loc_data[loc][k] += vals[k]

    # Create DataFrame
    data_list = []
    for loc, vals in loc_data.items():
        data_list.append([loc] + vals)
        
    df_result = pd.DataFrame(data_list, columns=['Localidad'] + age_groups)
    df_result = df_result.sort_values(by='TOTAL', ascending=False)
    
    # Add Global Total Row
    total_row = ['TOTAL GLOBAL']
    for age in age_groups:
        total_row.append(df_result[age].sum())
    
    df_result.loc[len(df_result)] = total_row
    
    # Save to Excel
    output_excel = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\INFORMES\Dosis_por_Localidad_y_Edad_Mezquital_2026.xlsx"
    
    with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
        df_result.to_excel(writer, index=False, sheet_name='Desglose')
        
        workbook = writer.book
        worksheet = writer.sheets['Desglose']
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
        total_format = workbook.add_format({'bold': True, 'bg_color': '#F2F2F2', 'border': 1})
        
        for col_num, value in enumerate(df_result.columns):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 15)
            
        # Bold last row
        for col_num, value in enumerate(df_result.iloc[-1]):
            worksheet.write(len(df_result), col_num, value, total_format)

    print(f"Excel saved: {output_excel}")

except Exception as e:
    print(f"Error: {e}")
