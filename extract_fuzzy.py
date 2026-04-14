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
    # limit spacing
    name = " ".join(name.split())
    return name

new_crono_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\CRONOGRAMAS DE VISITAS ESCUELAS\CRONOGRAMA DE ESCUELAS JURISDCCION 2.xlsx"
tops_path = r"C:\Users\aicil\.gemini\antigravity\scratch\VPH25-26_TOP100PTES_copy2.xlsx"

try:
    df_new = pd.read_excel(new_crono_path)
    df_tops = pd.read_excel(tops_path)
    
    unique_schools = df_tops['N_CCT'].dropna().astype(str).unique()
    school_map = {normalize_school_name(s): s for s in unique_schools}
    norm_school_list = list(school_map.keys())
    
    def extract_from_all(df):
        found_matches = []
        date_pattern = re.compile(r'(\d{1,2}\s*(?:DE\s|-)?\s*(?:ABRIL|MAYO)[^\w]*)')
        
        # Iterate all rows and all columns
        for _, row in df.iterrows():
            # Usually the 'UNIDADES' column has the medical unit
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
                for chunk in chunks:
                    norm_chunk = normalize_school_name(chunk)
                    if not norm_chunk:
                        continue
                    
                    # date extraction
                    date_match = date_pattern.search(chunk.upper())
                    if date_match:
                        current_date = date_match.group(1).strip()
                        last_seen_date = current_date
                        # remove date from norm_chunk to improve matching
                        norm_chunk = re.sub(date_pattern, ' ', norm_chunk).strip()
                    else:
                        current_date = last_seen_date
                    
                    if len(norm_chunk) > 3:
                        matches = difflib.get_close_matches(norm_chunk, norm_school_list, n=1, cutoff=0.7)
                        if matches:
                            matched_norm = matches[0]
                            original_school_name = school_map[matched_norm]
                            found_matches.append({
                                'ESCUELA_MATCH': original_school_name,
                                'FECHA_VISITA': current_date,
                                'UNIDAD_MEDICA': unidad,
                                'JURISDICCION': 2 # Since it says JURISDICCION 2
                            })
        return found_matches

    matches = extract_from_all(df_new)
    print(f"Total extracted: {len(matches)}")
    print(matches[:5])
    
    # Save a CSV with the extracts to review
    pd.DataFrame(matches).to_csv(r"C:\Users\aicil\.gemini\antigravity\scratch\extracted.csv", index=False)
except Exception as e:
    print(f"Error: {e}")
