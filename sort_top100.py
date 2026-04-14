import pandas as pd
import os

os.system('taskkill /F /IM excel.exe')

out_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\VPH25-26_TOP100PTES.xlsx"
crono_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\CRONOGRAMA_INTEGRADO_VPH_2025_12abril2026.xlsx"

try:
    df_tops = pd.read_excel(out_path)
    df_crono = pd.read_excel(crono_path)
    
    # If JURISDICCION is not in tops, map it from crono
    if 'JURISDICCION' not in df_tops.columns or 'INSTITUCION' not in df_tops.columns:
        df_tops['match_esc'] = df_tops['N_CCT'].astype(str).str.strip().str.upper()
        df_crono['match_esc'] = df_crono['ESCUELA'].astype(str).str.strip().str.upper()
        crono_unique = df_crono.drop_duplicates(subset=['match_esc'])
        
        mapping_cols = ['match_esc']
        if 'JURISDICCION' not in df_tops.columns and 'JURISDICCION' in df_crono.columns:
            mapping_cols.append('JURISDICCION')
        if 'INSTITUCION' not in df_tops.columns and 'INSTITUCION' in df_crono.columns:
            mapping_cols.append('INSTITUCION')
            
        mapping = crono_unique[mapping_cols]
        df_tops = pd.merge(df_tops, mapping, on='match_esc', how='left')
        df_tops = df_tops.drop(columns=['match_esc'])

    # Determine sort columns
    sort_cols = []
    if 'INSTITUCION' in df_tops.columns:
        sort_cols.append('INSTITUCION')
    elif 'INSTITUCION_SALUD' in df_tops.columns:
        sort_cols.append('INSTITUCION_SALUD')
        
    if 'JURISDICCION' in df_tops.columns:
        sort_cols.append('JURISDICCION')
    
    if sort_cols:
        df_tops = df_tops.sort_values(by=sort_cols)
        
    df_tops.to_excel(out_path, index=False)
    print(f"Sorted by {sort_cols}")
    os.startfile(out_path)

except Exception as e:
    print(f"Error: {e}")
