import pandas as pd
import sys
import re
import os
from openpyxl import load_workbook

def parse_date_from_filename(filename):
    basename = os.path.basename(filename)
    m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', basename)
    if m:
        return f"{m.group(1)}/{m.group(2)}/{m.group(3)}"
    return None

def process_daily_file(filepath):
    df = pd.read_excel(filepath, sheet_name="Existencias en puntos")
    
    # Clean up column names for easier access
    df.columns = ['Biológico', 'Almacén', 'Puntos', 'Extra']
    
    # Store results here
    results = {}
    
    # Get global totals first (top of the file)
    sr_global = df[df['Biológico'].astype(str).str.contains(r'SR\s*\(Doble viral', na=False, regex=True)].iloc[0]
    srp_global = df[df['Biológico'].astype(str).str.contains(r'SRP\s*\(Triple viral', na=False, regex=True)].iloc[0]
    
    total_sr_almacen = int(sr_global['Almacén']) if pd.notna(sr_global['Almacén']) else 0
    total_sr_puntos = int(sr_global['Puntos']) if pd.notna(sr_global['Puntos']) else 0
    total_srp_almacen = int(srp_global['Almacén']) if pd.notna(srp_global['Almacén']) else 0
    total_srp_puntos = int(srp_global['Puntos']) if pd.notna(srp_global['Puntos']) else 0
    
    results['TOTAL GENERAL'] = {
        'SR ALMACÉN': total_sr_almacen, 'SR PUNTOS': total_sr_puntos, 'TOTAL SR': total_sr_almacen + total_sr_puntos,
        'SRP ALMACÉN': total_srp_almacen, 'SRP PUNTOS': total_srp_puntos, 'TOTAL SRP': total_srp_almacen + total_srp_puntos,
        'GRAN TOTAL': total_sr_almacen + total_sr_puntos + total_srp_almacen + total_srp_puntos
    }
    
    # Find jurisdiction rows
    current_jurisdiction = None
    jurisdictions = ['JURISDICCIÓN No. 1', 'JURISDICCIÓN No.2', 'JURISDICCIÓN No. 3', 'JURISDICCIÓN No. 4']
    
    for _, row in df.iterrows():
        val = str(row['Biológico']).strip()
        if 'JURISDICCIÓN' in val.upper() or 'JURISDICCION' in val.upper():
            # Keep standard names
            if '1' in val: current_jurisdiction = 'JURISDICCIÓN No. 1'
            elif '2' in val: current_jurisdiction = 'JURISDICCIÓN No. 2' # Fix space
            elif '3' in val: current_jurisdiction = 'JURISDICCIÓN No. 3'
            elif '4' in val: current_jurisdiction = 'JURISDICCIÓN No. 4'
            else: current_jurisdiction = val
            
            if current_jurisdiction not in results:
                results[current_jurisdiction] = {
                    'SR ALMACÉN': 0, 'SR PUNTOS': 0, 'TOTAL SR': 0,
                    'SRP ALMACÉN': 0, 'SRP PUNTOS': 0, 'TOTAL SRP': 0
                }
        elif pd.notna(current_jurisdiction):
            if re.search(r'SR\s*\(Doble viral', val, flags=re.IGNORECASE):
                almacen = int(row['Almacén']) if pd.notna(row['Almacén']) else 0
                puntos = int(row['Puntos']) if pd.notna(row['Puntos']) else 0
                results[current_jurisdiction]['SR ALMACÉN'] = almacen
                results[current_jurisdiction]['SR PUNTOS'] = puntos
                results[current_jurisdiction]['TOTAL SR'] = almacen + puntos
            elif re.search(r'SRP\s*\(Triple viral', val, flags=re.IGNORECASE):
                almacen = int(row['Almacén']) if pd.notna(row['Almacén']) else 0
                puntos = int(row['Puntos']) if pd.notna(row['Puntos']) else 0
                results[current_jurisdiction]['SRP ALMACÉN'] = almacen
                results[current_jurisdiction]['SRP PUNTOS'] = puntos
                results[current_jurisdiction]['TOTAL SRP'] = almacen + puntos
                
    return results

def test():
    fp = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\INFORME\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS\INF MÓDULOS EXISTENCIAS DOSIS APLICADAS 10.03.2026.xlsx"
    res = process_daily_file(fp)
    import json
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    test()
