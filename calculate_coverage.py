import pandas as pd
import numpy as np

files = {
    'csv': r'c:\Descargas_SRP\SRP-SR-2025_10-04-2026 09-26-01.csv',
    'poblacion': r'c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\COBERTURA DE VACUNACIÓN\TABLERO SARAMPION V2\Poblacion municipio edad simple y sexo Mexico 2026 CENJSIA EGM.xlsx',
    'cubo_total': 669
}

def calculate_mezquital_coverage():
    # ── 1. POBLACION EXTRACTION ───────────────────────────────────────────
    print("Extracting Mezquital population...")
    df_pob = pd.read_excel(files['poblacion'], sheet_name='Durango', header=None)
    
    # Find the header row containing 'Mezquital'
    header_idx = -1
    mez_col = -1
    for i in range(50):
        row = df_pob.iloc[i].astype(str)
        if row.str.contains('Mezquital', case=False).any():
            header_idx = i
            mez_col = row[row.str.contains('Mezquital', case=False)].index[0]
            print(f"Mezquital found in Column {mez_col} (index {i})")
            break
            
    if header_idx == -1:
        raise ValueError("Mezquital not found in Poblacion file.")

    # Find Hombres and Mujeres blocks
    # They usually have 'Hombres' and 'Mujeres' in column 0
    col0 = df_pob[0].astype(str)
    h_idx = col0[col0.str.contains('Hombres', case=False)].index[0]
    m_idx = col0[col0.str.contains('Mujeres', case=False)].index[0]
    print(f"Hombres start: {h_idx}, Mujeres start: {m_idx}")
    
    pop = {}
    for age in range(101):
        try:
            h_val = float(df_pob.iloc[h_idx + 1 + age, mez_col])
        except:
            h_val = 0
            
        try:
            m_val = float(df_pob.iloc[m_idx + 1 + age, mez_col])
        except:
            m_val = 0
            
        pop[age] = h_val + m_val
    
    # ── 2. META CALCULATION ───────────────────────────────────────────────
    metas = {
        '6 a 11 meses':          0.5 * pop[0],
        '1 año':                 1.0 * pop[1],
        '18 meses':              1.0 * pop[1],
        'Rezagados 2 a 12 años': 0.5 * sum(pop[a] for a in range(2, 13)),
        '13 a 19 años':           0.5 * sum(pop[a] for a in range(13, 20)),
        '20 a 39 años':           0.5 * sum(pop[a] for a in range(20, 40)),
        '40 a 49 años':           0.5 * sum(pop[a] for a in range(40, 50))
    }
    
    # ── 3. CUBO DOSES ─────────────────────────────────────────────────────
    total_meta = sum(metas.values())
    jan_may_doses = {g: (m / total_meta) * files['cubo_total'] for g, m in metas.items()}
    
    # ── 4. CSV DOSES ───────────────────────────────────────────────────────
    print("Reading CSV doses...")
    df_csv = pd.read_csv(files['csv'], encoding='latin-1', sep=',')
    df_csv.columns = [c.strip() for c in df_csv.columns]
    mez_csv = df_csv[df_csv['MUNICIPIO'].str.contains('MEZQUITAL', case=False, na=False)]
    
    csv_groups = {
        '6 a 11 meses':          ['SRP 6 A 11 MESES PRIMERA', 'SR 6 A 11 MESES PRIMERA'],
        '1 año':                 ['SRP 1 ANIO  PRIMERA', 'SR 1 ANIO PRIMERA'],
        '18 meses':              ['SRP 18 MESES SEGUNDA', 'SR 18 MESES SEGUNDA'],
        'Rezagados 2 a 12 años': [
            'SRP 2 A 5 ANIOS PRIMERA', 'SRP 6 ANIOS PRIMERA', 'SRP 7 A 9 ANIOS PRIMERA', 'SRP 10 A 12 ANIOS PRIMERA',
            'SRP 2 A 5 ANIOS SEGUNDA', 'SRP 6 ANIOS SEGUNDA', 'SRP 7 A 9 ANIOS SEGUNDA', 'SRP 10 A 12 ANIOS SEGUNDA',
            'SR 2 A 5 ANIOS PRIMERA', 'SR 6 ANIOS PRIMERA', 'SR 7 A 9 ANIOS PRIMERA', 'SR 10 A 12 ANIOS PRIMERA',
            'SR 2 A 5 ANIOS SEGUNDA', 'SR 6 ANIOS SEGUNDA', 'SR 7 A 9 ANIOS SEGUNDA', 'SR 10 A 12 ANIOS SEGUNDA'
        ],
        '13 a 19 años': [
            'SRP 13 A 19 ANIOS PRIMERA', 'SRP 13 A 19 ANIOS SEGUNDA', 'SRP 10 A 19 ANIOS PRIMERA', 'SRP 10 A 19 ANIOS SEGUNDA',
            'SR 13 A 19 ANIOS PRIMERA', 'SR 13 A 19 ANIOS SEGUNDA', 'SR 10 A 19 ANIOS PRIMERA', 'SR 10 A 19 ANIOS SEGUNDA'
        ],
        '20 a 39 años': [
            'SRP 20 A 29 ANIOS PRIMERA', 'SRP 20 A 29 ANIOS SEGUNDA', 'SRP 30 A 39 ANIOS PRIMERA', 'SRP 30 A 39 ANIOS SEGUNDA',
            'SR 20 A 29 ANIOS PRIMERA', 'SR 20 A 29 ANIOS SEGUNDA', 'SR 30 A 39 ANIOS PRIMERA', 'SR 30 A 39 ANIOS SEGUNDA'
        ],
        '40 a 49 años': [
            'SRP 40 A 49 ANIOS PRIMERA', 'SRP 40 A 49 ANIOS SEGUNDA',
            'SR 40 A 49 ANIOS PRIMERA', 'SR 40 A 49 ANIOS SEGUNDA'
        ]
    }
    
    current_csv_doses = {}
    for g, cols in csv_groups.items():
        valid_cols = [c for c in cols if c in mez_csv.columns]
        val = mez_csv[valid_cols].apply(pd.to_numeric, errors='coerce').fillna(0).sum().sum()
        current_csv_doses[g] = val

    # ── 5. FINAL TABLE ────────────────────────────────────────────────────
    report = []
    for g in metas.keys():
        m_val = metas[g]
        cubo_v = jan_may_doses[g]
        csv_v = current_csv_doses[g]
        tot = cubo_v + csv_v
        report.append({
            'Grupo': g,
            'Meta': round(m_val),
            'Dosis Jan-May 2025': round(cubo_v),
            'Dosis May 2025-Now': round(csv_v),
            'Dosis Total': round(tot),
            'Cobertura (%)': round((tot/m_val)*100, 2) if m_val > 0 else 0
        })
    return pd.DataFrame(report)

if __name__ == "__main__":
    try:
        df = calculate_mezquital_coverage()
        print("\nREPORTE DE COBERTURA - MEZQUITAL")
        print(df.to_string(index=False))
        df.to_csv(r'C:\Users\aicil\.gemini\antigravity\scratch\reporte_cobertura_mezquital_final.csv', index=False)
    except Exception as e:
        print(f"Error in calculation: {e}")
