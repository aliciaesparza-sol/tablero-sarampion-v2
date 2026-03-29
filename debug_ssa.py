import csv
from collections import defaultdict

file_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\ACUSES DE RECIBOS DE VACUNA 2025\PTS SANAS 2025\INFORME COVID-19 CAMPAÑA 2025-2026\INFLUENZA-COVID-NEUMO 10-03-2026 02-45-57.csv'

dates_ssa = defaultdict(lambda: {'P': 0, 'M': 0})
s_moderna = 'SUMA POBLACION BLANCO COVID MODERNA'
s_pfizer = 'SUMA POBLACION BLANCO COVID PFIZER'
r_moderna = 'SUMA GRUPO DE RIESGO COVID MODERNA'
r_pfizer = 'SUMA GRUPO DE RIESGO COVID PFIZER'

with open(file_path, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('INSTITUCION', '').upper().strip() != 'SSA':
            continue
        
        date_str = row.get('FECHA DEL DOCUMENTO', '')
        if not date_str:
            continue
            
        try:
            m = int(float(row[s_moderna])) + int(float(row[r_moderna]))
            p = int(float(row[s_pfizer])) + int(float(row[r_pfizer]))
            dates_ssa[date_str]['P'] += p
            dates_ssa[date_str]['M'] += m
        except:
            pass

print("Date Breakdown for SSA:")
sorted_dates = sorted(dates_ssa.keys())
for d in sorted_dates:
    if '2026' in d:
        print(f"{d} -> Pfizer: {dates_ssa[d]['P']}, Moderna: {dates_ssa[d]['M']}")
