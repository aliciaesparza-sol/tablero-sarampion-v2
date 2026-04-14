import pandas as pd

tops_path = r"C:\Users\aicil\.gemini\antigravity\scratch\VPH25-26_TOP100PTES_copy2.xlsx"
crono_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\CRONOGRAMA_INTEGRADO_VPH_2025_12abril2026.xlsx"
out_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\VPH25-26_TOP100PTES.xlsx"

try:
    df_tops = pd.read_excel(tops_path)
    df_crono = pd.read_excel(crono_path)
    
    # We will match on BOTH locality and school name to avoid duplicates
    # For df_tops: N_LOCALIDAD and N_CCT
    # For df_crono: N_LOCALIDAD and ESCUELA
    df_tops['match_loc'] = df_tops['N_LOCALIDAD'].astype(str).str.strip().str.upper()
    df_tops['match_esc'] = df_tops['N_CCT'].astype(str).str.strip().str.upper()
    
    df_crono['match_loc'] = df_crono['N_LOCALIDAD'].astype(str).str.strip().str.upper()
    df_crono['match_esc'] = df_crono['ESCUELA'].astype(str).str.strip().str.upper()
    
    # Since cronograma might have duplicate school visits (e.g. multiple days), let's keep the first or unique scheduled days
    crono_unique = df_crono.drop_duplicates(subset=['match_loc', 'match_esc'])
    
    mapping = crono_unique[['match_loc', 'match_esc', 'FECHA_VISITA']]
    if 'UNIDAD_MEDICA' in df_crono.columns:
        mapping['UNIDAD_MEDICA'] = crono_unique['UNIDAD_MEDICA']
    
    df_cleaned = pd.merge(df_tops, mapping, on=['match_loc', 'match_esc'], how='inner')
    
    # remove match columns
    df_cleaned = df_cleaned.drop(columns=['match_loc', 'match_esc'])
    
    print(f"Original size: {len(df_tops)}, Cleaned size: {len(df_cleaned)}")
    
    # Try overwriting original since user might have closed it
    try:
         df_cleaned.to_excel(out_path, index=False)
         print(f"Successfully overwrote original file: {out_path}")
    except PermissionError:
         print("Original file is open, saving to _LIMPIO instead.")
         alt_path = out_path.replace(".xlsx", "_LIMPIO2.xlsx")
         df_cleaned.to_excel(alt_path, index=False)
         print(f"Saved to {alt_path}")

except Exception as e:
    print(f"Error: {e}")
