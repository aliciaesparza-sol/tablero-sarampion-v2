import pandas as pd
import re
import difflib
import unicodedata

def remove_accents(input_str):
    if not isinstance(input_str, str):
        return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).upper()

def normalize_school_name(name):
    name = remove_accents(name)
    name = name.replace('FCO ', 'FRANCISCO ')
    name = name.replace('FCO. ', 'FRANCISCO ')
    name = name.replace('GPE ', 'GUADALUPE ')
    name = name.replace('GRAL ', 'GENERAL ')
    name = name.replace('GRAL. ', 'GENERAL ')
    name = name.replace('LIC ', 'LICENCIADO ')
    name = name.replace('LIC. ', 'LICENCIADO ')
    name = name.replace(' T.M ', ' ')
    name = name.replace(' T.V ', ' ')
    name = name.replace(' TV ', ' ')
    name = re.sub(r'[^A-Z0-9 ]', ' ', name)
    name = " ".join(name.split())
    return name

new_crono_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\CRONOGRAMAS DE VISITAS ESCUELAS\CRONOGRAMA DE ESCUELAS JURISDCCION 2.xlsx"
tops_path = r"C:\Users\aicil\.gemini\antigravity\scratch\VPH25-26_TOP100PTES_copy2.xlsx"

df_new = pd.read_excel(new_crono_path)
df_tops = pd.read_excel(tops_path)

unique_schools = df_tops['N_CCT'].dropna().astype(str).unique()
school_map = {normalize_school_name(s): s for s in unique_schools}
norm_school_list = list(school_map.keys())

def extract_from_all(df):
    found_matches = []
    # match spaces optionally before and after "DE" 
    date_pattern = re.compile(r'(\d{1,2}\s*(?:DE\s|-)?\s*(?:ABRIL|MAYO)[^\w]*)')
    
    for _, row in df.iterrows():
        unidad = row.get('UNIDADES', '')
        unidad = str(unidad).strip() if pd.notna(unidad) else ''
        
        for col in df.columns:
            if col in ['UNIDADES', 'FECHAS']:
                continue
            
            text = row[col]
            if pd.isna(text) or not isinstance(text, str):
                continue
            
            text_clean = text.replace('.', ' , ').replace(' Y ', ' , ')
            chunks = [c.strip() for c in text_clean.split(',') if c.strip()]
            
            last_seen_date = None
            # Do a backward pass or forward pass? Usually the date follows the school name
            for chunk in chunks:
                norm_chunk = normalize_school_name(chunk)
                if not norm_chunk:
                    continue
                
                date_match = date_pattern.search(chunk.upper())
                current_date = last_seen_date
                if date_match:
                    current_date = date_match.group(1).strip()
                    last_seen_date = current_date
                    norm_chunk = re.sub(date_pattern, ' ', norm_chunk).strip()
                
                if len(norm_chunk) > 3:
                    matches = difflib.get_close_matches(norm_chunk, norm_school_list, n=1, cutoff=0.7)
                    if matches:
                        matched_norm = matches[0]
                        original_school_name = school_map[matched_norm]
                        found_matches.append({
                            'match_esc': original_school_name.upper().strip(),
                            'FECHA_VISITA': current_date, # assign current date found for this chunk or last seen
                            'UNIDAD_MEDICA': unidad,
                            'JURISDICCION': 2
                        })
    return found_matches

matches = extract_from_all(df_new)

# Now merge into clean file
clean_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\ESCUELAS\VPH25-26_TOP100PTES.xlsx"
import os
os.system('taskkill /F /IM excel.exe')

df_clean = pd.read_excel(clean_path)

# Prepare df of missing ones
df_matches = pd.DataFrame(matches)

# To get the full row from tops, we merge df_matches with df_tops
df_tops['match_esc'] = df_tops['N_CCT'].astype(str).str.strip().str.upper()

# inner join to get the full row details for the matched schools
df_matched_full = pd.merge(df_tops, df_matches, on='match_esc', how='inner')
df_matched_full = df_matched_full.drop_duplicates(subset=['match_esc'])

# Drop match_esc from both
df_matched_full = df_matched_full.drop(columns=['match_esc'])
# append to df_clean
df_combined = pd.concat([df_clean, df_matched_full], ignore_index=True)

# sort
sort_cols = []
if 'INSTITUCION' in df_combined.columns:
    sort_cols.append('INSTITUCION')
elif 'INSTITUCION_SALUD' in df_combined.columns:
    sort_cols.append('INSTITUCION_SALUD')
if 'JURISDICCION' in df_combined.columns:
    sort_cols.append('JURISDICCION')

if sort_cols:
    df_combined = df_combined.sort_values(by=sort_cols)

df_combined.to_excel(clean_path, index=False)
print(f"Added {len(df_matched_full)} schools from Jurisdiccion 2.")
os.startfile(clean_path)
