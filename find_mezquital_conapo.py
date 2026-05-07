import pandas as pd

excel_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\POBLACIÓN\POBLACION 2026\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx"

try:
    df = pd.read_excel(excel_path, sheet_name='Durango')
    # Find rows where "Mezquital" is mentioned
    mask = df.apply(lambda row: row.astype(str).str.contains('Mezquital', case=False).any(), axis=1)
    matching_rows = df[mask]
    
    if not matching_rows.empty:
        print("--- MATCHING ROWS FOR MEZQUITAL ---")
        print(matching_rows.iloc[:, :10]) # Show first 10 cols
        
        # Get the row index
        idx = matching_rows.index[0]
        # Show some context rows
        print("\n--- CONTEXT AROUND MATCH ---")
        print(df.iloc[idx:idx+30, :10])
    else:
        print("Mezquital not found in 'Durango' sheet.")

except Exception as e:
    print(f"Error: {e}")
