import csv

file_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\ACUSES DE RECIBOS DE VACUNA 2025\PTS SANAS 2025\INFORME COVID-19 CAMPAÑA 2025-2026\INFLUENZA-COVID-NEUMO 10-03-2026 02-45-57.csv'

with open(file_path, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    feb_p = 0
    feb_m = 0
    mar_p = 0
    mar_m = 0
    
    for row in reader:
        if row.get('INSTITUCION', '').upper().strip() == 'SSA':
            date_str = row.get('FECHA DEL DOCUMENTO', '')
            # Try to handle - and / and different orders
            month = None
            if '-' in date_str:
                parts = date_str.split('-')
                if len(parts[0]) == 4: # YYYY-MM-DD
                    month = int(parts[1])
                    year = int(parts[0])
                else: # DD-MM-YYYY
                    month = int(parts[1])
                    year = int(parts[2])
            elif '/' in date_str:
                parts = date_str.split('/')
                # Assume DD/MM/YYYY or YYYY/MM/DD
                if len(parts[0]) == 4:
                    month = int(parts[1])
                    year = int(parts[0])
                else:
                    month = int(parts[1])
                    year = int(parts[2])
            
            if not month: continue
            
            # Check for Pfizer/Moderna
            s_moderna = float(row.get('SUMA POBLACION BLANCO COVID MODERNA', 0))
            s_pfizer = float(row.get('SUMA POBLACION BLANCO COVID PFIZER', 0))
            r_moderna = float(row.get('SUMA GRUPO DE RIESGO COVID MODERNA', 0))
            r_pfizer = float(row.get('SUMA GRUPO DE RIESGO COVID PFIZER', 0))
            
            p = s_pfizer + r_pfizer
            m = s_moderna + r_moderna
            
            if month == 2:
                feb_p += p
                feb_m += m
            elif month == 3:
                mar_p += p
                mar_m += m

print(f"DEBUG TOTAL SSA: FEB Pfizer: {feb_p}, Moderna: {feb_m} | MAR Pfizer: {mar_p}, Moderna: {mar_m}")
