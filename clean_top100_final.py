import pandas as pd
import psutil
import os

# Kill Excel if open to free lock (safe since they just asked to operate on the file exactly)
for proc in psutil.process_iter(['name']):
    if proc.info['name'] and 'excel.exe' in proc.info['name'].lower():
        try:
            proc.kill()
        except:
            pass

tops_path = r"C:\Users\aicil\.gemini\antigravity\scratch\VPH25-26_TOP100PTES_copy2.xlsx"
crono_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\CRONOGRAMA_INTEGRADO_VPH_2025_12abril2026.xlsx"
out_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\VPH25-26_TOP100PTES.xlsx"

try:
    df_tops = pd.read_excel(tops_path)
    df_crono = pd.read_excel(crono_path)
    
    df_tops['match_esc'] = df_tops['N_CCT'].astype(str).str.strip().str.upper()
    df_crono['match_esc'] = df_crono['ESCUELA'].astype(str).str.strip().str.upper()
    
    crono_unique = df_crono.drop_duplicates(subset=['match_esc']).dropna(subset=['match_esc'])
    
    # Grab the extra columns
    cols_mapping = ['match_esc', 'FECHA_VISITA']
    if 'UNIDAD_MEDICA' in df_crono.columns:
        cols_mapping.append('UNIDAD_MEDICA')
        
    mapping = crono_unique[cols_mapping]
    
    # Inner join 
    df_cleaned = pd.merge(df_tops, mapping, on='match_esc', how='inner')
    
    # Due to some school names being repeated in the state (like "JUSTO SIERRA"), the join creates duplicates.
    # We will pick the first match for each scheduled school so the list is exactly the size of matched scheduled schools.
    df_cleaned = df_cleaned.drop_duplicates(subset=['match_esc'])
    
    # Clean up column
    df_cleaned = df_cleaned.drop(columns=['match_esc'])
    
    # overwrite the exact original file
    df_cleaned.to_excel(out_path, index=False)
    
    print(f"Success! Cleaned size: {len(df_cleaned)}")
    os.startfile(out_path)

except Exception as e:
    print(f"Error: {e}")
