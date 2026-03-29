import csv
from collections import defaultdict

file_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\ACUSES DE RECIBOS DE VACUNA 2025\PTS SANAS 2025\INFORME COVID-19 CAMPAÑA 2025-2026\INFLUENZA-COVID-NEUMO 10-03-2026 02-45-57.csv'

stats = defaultdict(lambda: {'P': 0, 'M': 0})
s_moderna = 'SUMA POBLACION BLANCO COVID MODERNA'
s_pfizer = 'SUMA POBLACION BLANCO COVID PFIZER'
r_moderna = 'SUMA GRUPO DE RIESGO COVID MODERNA'
r_pfizer = 'SUMA GRUPO DE RIESGO COVID PFIZER'

with open(file_path, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        date_str = row.get('FECHA DEL DOCUMENTO', '')
        month = None
        if '-' in date_str: month = int(date_str.split('-')[1])
        elif '/' in date_str: month = int(date_str.split('/')[1])
        
        if month in [2, 3]:
            try:
                inst = row.get('INSTITUCION', 'UNKNOWN').upper().strip()
                p = float(row.get(s_pfizer, 0)) + float(row.get(r_pfizer, 0))
                m = float(row.get(s_moderna, 0)) + float(row.get(r_moderna, 0))
                stats[inst]['P'] += p
                stats[inst]['M'] += m
            except: pass

for inst, d in stats.items():
    print(f"{inst} -> Febrero/Marzo TOTAL: Pfizer: {d['P']}, Moderna: {d['M']}")
