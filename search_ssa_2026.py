import csv

file_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\ACUSES DE RECIBOS DE VACUNA 2025\PTS SANAS 2025\INFORME COVID-19 CAMPAÑA 2025-2026\INFLUENZA-COVID-NEUMO 10-03-2026 02-45-57.csv'
s_moderna = 'SUMA POBLACION BLANCO COVID MODERNA'
s_pfizer = 'SUMA POBLACION BLANCO COVID PFIZER'
r_moderna = 'SUMA GRUPO DE RIESGO COVID MODERNA'
r_pfizer = 'SUMA GRUPO DE RIESGO COVID PFIZER'
total_col = 'TOTAL DE DOSIS COVID'

records = []
with open(file_path, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('INSTITUCION', '').upper().strip() == 'SSA':
            date_str = row.get('FECHA DEL DOCUMENTO', '')
            if '2026-02' in date_str or '2026-03' in date_str:
                try:
                    t = float(row[total_col])
                    if t > 0:
                        m = float(row[s_moderna]) + float(row[r_moderna])
                        p = float(row[s_pfizer]) + float(row[r_pfizer])
                        records.append(f"Date: {date_str}, T:{t}, M:{m}, P:{p}")
                except:
                    pass

if not records:
    print("NO NON-ZERO RECORDS FOUND FOR SSA IN FEB/MAR 2026")
else:
    for rec in records:
        print(rec)
