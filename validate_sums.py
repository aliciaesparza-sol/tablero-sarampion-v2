import csv

file_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\ACUSES DE RECIBOS DE VACUNA 2025\PTS SANAS 2025\INFORME COVID-19 CAMPAÑA 2025-2026\INFLUENZA-COVID-NEUMO 10-03-2026 02-45-57.csv'

with open(file_path, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    total_mismatch = 0
    ssa_records = 0
    for row in reader:
        if row.get('INSTITUCION', '').upper().strip() == 'SSA':
            ssa_records += 1
            try:
                m_b = float(row.get('SUMA POBLACION BLANCO COVID MODERNA', 0))
                p_b = float(row.get('SUMA POBLACION BLANCO COVID PFIZER', 0))
                o_b = float(row.get('SUMA POBLACION BLANCO COVID OTRA', 0))
                tot_b = float(row.get('SUMA POBLACION BLANCO COVID', 0))
                
                m_r = float(row.get('SUMA GRUPO DE RIESGO COVID MODERNA', 0))
                p_r = float(row.get('SUMA GRUPO DE RIESGO COVID PFIZER', 0))
                o_r = float(row.get('SUMA GRUPO DE RIESGO COVID OTRA', 0))
                tot_r = float(row.get('SUMA GRUPO DE RIESGO COVID', 0))
                
                if abs((m_b + p_b + o_b) - tot_b) > 0.01:
                    total_mismatch += 1
                if abs((m_r + p_r + o_r) - tot_r) > 0.01:
                    total_mismatch += 1
            except:
                pass

print(f"SSA records checked: {ssa_records}")
print(f"Total mismatches found: {total_mismatch}")
