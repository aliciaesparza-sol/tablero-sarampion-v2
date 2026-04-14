import pandas as pd
import re

new_crono_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\VPH\CAMPAÑA VPH 2025\CRONOGRAMAS DE VISITAS ESCUELAS\CRONOGRAMA DE ESCUELAS JURISDCCION 2.xlsx"
tops_path = r"C:\Users\aicil\.gemini\antigravity\scratch\VPH25-26_TOP100PTES_copy2.xlsx"

try:
    df_new = pd.read_excel(new_crono_path)
    df_tops = pd.read_excel(tops_path)
    
    # Preprocess list of all schools
    # Sort by length descending, so we match longer names first ("18 DE MARZO" vs "MARZO")
    unique_schools = df_tops['N_CCT'].dropna().astype(str).str.strip().str.upper().unique()
    unique_schools = sorted(list(set(unique_schools)), key=len, reverse=True)
    
    def extract_schools_and_dates(text):
        found = []
        if pd.isna(text):
            return found
        text = str(text).upper()
        # Clean text slightly
        text = text.replace('.', ' ').replace(',', ' , ').replace(' Y ', ' , ').replace('\n', ' ')
        
        # Split text by commas to get chunks
        chunks = [c.strip() for c in text.split(',') if c.strip()]
        
        date_pattern = re.compile(r'(\d{1,2}\s*(?:DE\s*)?(?:ABRIL|MAYO)[^\w]*)')
        
        last_seen_date = None
        for chunk in chunks:
            # find if date exists in chunk
            date_match = date_pattern.search(chunk)
            current_date = None
            if date_match:
                current_date = date_match.group(1).strip()
                last_seen_date = current_date
            else:
                current_date = last_seen_date
                
            # Search for school names in this chunk
            for school in unique_schools:
                # Need exact whole word match or at least boundary match
                if len(school) > 3 and school in chunk:
                    # check word boundaries
                    pattern = r'\b' + re.escape(school) + r'\b'
                    if re.search(pattern, chunk):
                        found.append((school, current_date))
                        # remove school from chunk so we don't match substrings
                        chunk = re.sub(pattern, " ", chunk)
                        
        return found
        
    print("Testing extraction on PRIMARIAS.1...")
    total_found = []
    for val in df_new['PRIMARIAS.1'].dropna().head(30):
        extracted = extract_schools_and_dates(val)
        print(f"Original: {val}")
        print(f"Extracted: {extracted}\n")
        total_found.extend(extracted)
        
    print(f"Total extracted from top 30: {len(total_found)}")

except Exception as e:
    print(f"Error: {e}")
