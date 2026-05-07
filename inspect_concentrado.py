import pandas as pd

file_path = r"C:\Users\aicil\.gemini\antigravity\scratch\temp_file.xlsx"
sheet_name = "Concentrado"

try:
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=1)
    print(f"Columns in '{sheet_name}' (from header=1):")
    cols = df.columns.tolist()
    print(cols)
    
    # Search for locality column
    locality_col = None
    for col in cols:
        if any(term in str(col).upper() for term in ['LOCALIDAD', 'COMUNIDAD', 'NOMBRE']):
            locality_col = col
            break
            
    if locality_col:
        print(f"\nFound locality column: {locality_col}")
        localities = df[locality_col].dropna().unique().tolist()
        print(f"Number of unique localities: {len(localities)}")
        print("Sample localities:")
        for loc in localities[:30]:
            print(f"- {loc}")
    else:
        print("\nCould not find a locality column.")

except Exception as e:
    print(f"Error: {e}")
