import pandas as pd

tops_path = r"C:\Users\aicil\.gemini\antigravity\scratch\VPH25-26_TOP100PTES_copy2.xlsx"
crono_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\CRONOGRAMA_INTEGRADO_VPH_2025_12abril2026.xlsx"

try:
    df_tops = pd.read_excel(tops_path)
    df_crono = pd.read_excel(crono_path)
    
    # We want to match ESCUELA with N_CCT. 
    # Create an uppercase, stripped version for merging
    df_tops['match_key'] = df_tops['N_CCT'].astype(str).str.strip().str.upper()
    df_crono['match_key'] = df_crono['ESCUELA'].astype(str).str.strip().str.upper()
    
    # We map CLAVECCT, MUJ_4 (might be target pop for VPH), ALUMNOS_FALTANTES, COBERTURA_EST
    # Actually, let's just pick CLAVECCT and ALUMNOS_FALTANTES / MUJ_4 
    mapping = df_tops.drop_duplicates(subset='match_key')
    
    df_merged = pd.merge(df_crono, mapping[['match_key', 'CLAVECCT', 'MUJ_T', 'MUJ_4', 'COBERTURA_EST']], on='match_key', how='left')
    
    # drop match key
    df_merged = df_merged.drop(columns=['match_key'])
    
    # save back to cronograma integraddo
    df_merged.to_excel(crono_path, index=False)
    print("Success")

except Exception as e:
    print(f"Error: {e}")
