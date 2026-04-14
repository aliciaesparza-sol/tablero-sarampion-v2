import pandas as pd
import numpy as np

# Use the copy to read if the original might be locked
crono_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\CRONOGRAMA_INTEGRADO_VPH_2025_12abril2026.xlsx"
out_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\VPH25-26_TOP100PTES_LIMPIO.xlsx"

# Using the copy doc we made earlier to avoid permission issues when reading
tops_path = r"C:\Users\aicil\.gemini\antigravity\scratch\VPH25-26_TOP100PTES_copy2.xlsx"

try:
    df_tops = pd.read_excel(tops_path)
    df_crono = pd.read_excel(crono_path)
    
    df_tops['match_key'] = df_tops['N_CCT'].astype(str).str.strip().str.upper()
    df_crono['match_key'] = df_crono['ESCUELA'].astype(str).str.strip().str.upper()
    
    crono_scheduled = df_crono.dropna(subset=['match_key']).drop_duplicates(subset=['match_key'])
    
    cols_to_add = ['match_key', 'FECHA_VISITA', 'UNIDAD_MEDICA']
    if 'DIA_VISITA' in df_crono.columns:
        cols_to_add.append('DIA_VISITA')
        
    mapping = crono_scheduled[cols_to_add]
    
    # Inner join leaves only scheduled schools
    df_cleaned = pd.merge(df_tops, mapping, on='match_key', how='inner')
    
    # remove match_key
    df_cleaned = df_cleaned.drop(columns=['match_key'])
    
    original_size = len(df_tops)
    cleaned_size = len(df_cleaned)
    print(f"Original size: {original_size}, Cleaned size: {cleaned_size} (Scheduled schools found)")
    
    # Save back to a NEW CLEANED file to avoid file lock issues
    df_cleaned.to_excel(out_path, index=False)
    import os
    os.startfile(out_path)
    print("Success")

except Exception as e:
    print(f"Error: {e}")
