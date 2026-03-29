import pandas as pd
import json

files = {
    'pop': r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO SARAMPION\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx',
    'cubos': r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\Vacunacion_SRP_SR_Cubos_Enero-Mayo_2025.xlsx',
    'nominal': r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO SARAMPION\SRP-SR-2025_21-03-2026 08-11-38.csv'
}

analysis = {}

# 1. Population
try:
    df_pop = pd.read_excel(files['pop'], sheet_name='Durango', header=None)
    analysis['pop'] = {
        'head': df_pop.iloc[:20, :15].astype(str).values.tolist(),
        'columns': df_pop.iloc[7].astype(str).tolist() if len(df_pop) > 7 else []
    }
except Exception as e:
    analysis['pop_error'] = str(e)

# 2. Cubos
try:
    df_cubos = pd.read_excel(files['cubos'], nrows=10)
    analysis['cubos'] = {
        'columns': df_cubos.columns.tolist(),
        'head': df_cubos.astype(str).values.tolist()
    }
except Exception as e:
    analysis['cubos_error'] = str(e)

# 3. Nominal (CSV)
try:
    df_nom = pd.read_csv(files['nominal'], nrows=10, encoding='latin1')
    analysis['nominal'] = {
        'columns': df_nom.columns.tolist(),
        'head': df_nom.astype(str).values.tolist()
    }
except Exception as e:
    analysis['nominal_error'] = str(e)

with open(r'C:\Users\aicil\.gemini\antigravity\scratch\data_analysis_new.json', 'w', encoding='utf-8') as f:
    json.dump(analysis, f, indent=2, ensure_ascii=False)

print("Analysis complete.")
