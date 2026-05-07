import pandas as pd

excel_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\POBLACIÓN\POBLACION 2026\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx"

try:
    df = pd.read_excel(excel_path, sheet_name='Durango', header=None)
    col_idx = 15 # Mezquital
    
    hombres_idx = -1
    mujeres_idx = -1
    for i in range(len(df)):
        val = str(df.iloc[i, 0])
        if "Hombres" in val: hombres_idx = i
        if "Mujeres" in val: mujeres_idx = i
        
    def sum_all_ages(start_idx):
        total = 0
        for i in range(start_idx + 1, len(df)):
            try:
                age = int(float(df.iloc[i, 0]))
                pop = float(df.iloc[i, col_idx])
                total += pop
            except:
                if total > 0: break
        return total

    h_total = sum_all_ages(hombres_idx)
    m_total = sum_all_ages(mujeres_idx)
    print(f"Total Population Mezquital: {h_total + m_total}")
    
except Exception as e:
    print(f"Error: {e}")
