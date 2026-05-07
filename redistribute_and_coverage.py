import pandas as pd
import numpy as np

temp_excel = r"C:\Users\aicil\.gemini\antigravity\scratch\orig_temp.xlsx"
enriched_excel = r"C:\Users\aicil\.gemini\antigravity\scratch\Formato_Concentrado_Mezquital_2026_Updated.xlsx"

try:
    df = pd.read_excel(temp_excel, sheet_name="Concentrado", header=None)
    headers = df.iloc[2].tolist()
    
    # Age columns: 54-60. Total: 61. Locality: 4.
    age_cols = list(range(54, 61))
    total_col = 61
    loc_col = 4
    
    # 1. Calculate Overall Distribution
    total_by_age = np.zeros(len(age_cols))
    overall_total = 0
    
    data_rows = []
    for i in range(4, len(df)):
        loc = str(df.iloc[i, loc_col]).strip().upper()
        if loc == "NAN" or loc == "": continue
        
        ages = [pd.to_numeric(df.iloc[i, j], errors='coerce') for j in age_cols]
        ages = [a if not pd.isna(a) else 0 for a in ages]
        total = pd.to_numeric(df.iloc[i, total_col], errors='coerce')
        total = total if not pd.isna(total) else 0
        
        data_rows.append({"Loc": loc, "Ages": ages, "Total": total})
        
        if sum(ages) > 0:
            total_by_age += np.array(ages)
            overall_total += sum(ages)
            
    # Proportional weights
    weights = total_by_age / overall_total if overall_total > 0 else np.ones(len(age_cols)) / len(age_cols)
    print(f"Overall distribution weights: {weights}")
    
    # 2. Apply Proportional Distribution where missing
    final_loc_data = {}
    for entry in data_rows:
        loc = entry["Loc"]
        ages = entry["Ages"]
        total = entry["Total"]
        
        if total > 0 and sum(ages) == 0:
            # Distribute proportionally
            ages = (weights * total).round(0).astype(int).tolist()
            # Adjust last element to match total exactly
            diff = total - sum(ages)
            ages[-1] += diff
            
        if loc not in final_loc_data:
            final_loc_data[loc] = {"Ages": np.zeros(len(age_cols)), "Total": 0}
        
        final_loc_data[loc]["Ages"] += np.array(ages)
        final_loc_data[loc]["Total"] += total

    # 3. Get Population and Calculate Coverage
    # We use the enriched file for population
    df_pop = pd.read_excel(enriched_excel, sheet_name="Concentrado", header=None)
    # Manual corrections map (from previous turn)
    manual_pop = {
        "LAS JOYAS": 462, "STA MA. DE OCOTAN": 795, "STA. MA. DE OCOTAN": 795,
        "BAJÍO Y CENTRO": 255, "CARBONERAS": 226, "SAN MANUEL": 41
    }
    
    pop_map = {}
    for i in range(4, len(df_pop)):
        loc = str(df_pop.iloc[i, 4]).strip().upper()
        p = pd.to_numeric(df_pop.iloc[i, 82], errors='coerce')
        if not pd.isna(p) and p > 0:
            pop_map[loc] = max(pop_map.get(loc, 0), p)
            
    # Merge manual pops
    for k, v in manual_pop.items():
        pop_map[k] = v

    # 4. Final DataFrame
    age_labels = [headers[j] for j in age_cols]
    results = []
    for loc, data in final_loc_data.items():
        pop = pop_map.get(loc, 0)
        cov = (data["Total"] / pop * 100) if pop > 0 else 0
        results.append([loc] + data["Ages"].tolist() + [data["Total"], pop, cov])
        
    df_final = pd.DataFrame(results, columns=['Localidad'] + age_labels + ['TOTAL', 'POBLACION (INEGI)', 'COBERTURA (%)'])
    df_final = df_final.sort_values(by='TOTAL', ascending=False)
    
    # Global Total
    total_row = ['TOTAL GLOBAL']
    for col in df_final.columns[1:-1]: # Sum all except Locality and Coverage
        total_row.append(df_final[col].sum())
    
    # Recalculate global coverage
    # Wait, total population of municipality is better
    abs_total_pop = 53894
    actual_total = 20977 # As discussed before
    # Re-calculate total row carefully
    # Summing all columns except the last one (COBERTURA)
    sums = df_final.iloc[:, 1:-1].sum().tolist()
    # The absolute total pop is 53894. The sum of loc populations might be different.
    # User wants "cobertura global" in the table.
    global_cov = (actual_total / abs_total_pop * 100)
    total_row_final = ['TOTAL GLOBAL'] + sums[:-2] + [actual_total, abs_total_pop, global_cov]
    
    df_final.loc[len(df_final)] = total_row_final
    
    # Save to Excel
    output_excel = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\INFORMES\Dosis_por_Localidad_y_Edad_Proporcional_Mezquital_2026.xlsx"
    with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
        df_final.to_excel(writer, index=False, sheet_name='Desglose')
        # Formatting ...
        workbook = writer.book
        worksheet = writer.sheets['Desglose']
        header_f = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
        for c, v in enumerate(df_final.columns):
            worksheet.write(0, c, v, header_f)
            worksheet.set_column(c, c, 15)

    print(f"Excel saved: {output_excel}")

except Exception as e:
    print(f"Error: {e}")
