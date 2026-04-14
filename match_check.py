import pandas as pd

tops_path = r"C:\Users\aicil\.gemini\antigravity\scratch\VPH25-26_TOP100PTES_copy2.xlsx"
crono_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\CRONOGRAMA_INTEGRADO_VPH_2025_12abril2026.xlsx"

try:
    df_tops = pd.read_excel(tops_path)
    df_crono = pd.read_excel(crono_path)
    
    print("TOP100 ESCUELAS (N_CCT) sample:")
    print(df_tops['N_CCT'].head(10).tolist())
    
    print("\nCRONO ESCUELAS (ESCUELA) sample:")
    print(df_crono['ESCUELA'].head(10).tolist())
    
    # Check intersection
    tops_escuelas = set(df_tops['N_CCT'].dropna().str.strip().str.upper())
    crono_escuelas = set(df_crono['ESCUELA'].dropna().astype(str).str.strip().str.upper())
    
    intersection = tops_escuelas.intersection(crono_escuelas)
    print(f"\nUnique schools in VPH25-26_TOP100PTES.xlsx: {len(tops_escuelas)}")
    print(f"Unique schools in CRONOGRAMA: {len(crono_escuelas)}")
    print(f"Matches found: {len(intersection)}")
    
    # If not N_CCT, maybe CLAVECCT?
    crono_claves = set(df_crono['ESCUELA'].dropna().astype(str).str.strip().str.upper())
    tops_claves = set(df_tops['CLAVECCT'].dropna().astype(str).str.strip().str.upper())
    intersection_claves = tops_claves.intersection(crono_claves)
    print(f"Matches found using CLAVECCT: {len(intersection_claves)}")

except Exception as e:
    print(f"Error: {e}")
