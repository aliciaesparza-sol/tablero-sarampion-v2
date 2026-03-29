import csv
from collections import defaultdict

file_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\ACUSES DE RECIBOS DE VACUNA 2025\PTS SANAS 2025\INFORME COVID-19 CAMPAÑA 2025-2026\INFLUENZA-COVID-NEUMO 10-03-2026 02-45-57.csv'

months_map = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

requested_months = ['Octubre', 'Noviembre', 'Diciembre', 'Enero', 'Febrero', 'Marzo']
results = {
    'Pfizer': defaultdict(int),
    'Moderna': defaultdict(int)
}

with open(file_path, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    pfizer_cols = [h for h in reader.fieldnames if 'COVID' in h.upper() and 'PFIZER' in h.upper() and 'SUMA' not in h.upper()]
    moderna_cols = [h for h in reader.fieldnames if 'COVID' in h.upper() and 'MODERNA' in h.upper() and 'SUMA' not in h.upper()]
    
    for row in reader:
        institution = row.get('INSTITUCION', '').upper().strip()
        if institution != 'SSA':
            continue
            
        date_str = row.get('FECHA DEL DOCUMENTO')
        if not date_str:
            continue
        try:
            month_num = int(date_str.split('-')[1])
            month_name = months_map[month_num]
        except:
            continue
        
        if month_name in requested_months:
            for col in pfizer_cols:
                try:
                    val = row[col].strip()
                    if val:
                        results['Pfizer'][month_name] += int(float(val))
                except:
                    pass
            for col in moderna_cols:
                try:
                    val = row[col].strip()
                    if val:
                        results['Moderna'][month_name] += int(float(val))
                except:
                    pass

headers = ["VACUNA"] + requested_months + ["TOTAL"]
markdown = "# Resumen de Dosis Aplicadas Vacuna COVID-19 (SSA)\n\n"
markdown += "### Dosis Aplicadas - SSA\n\n"
markdown += "| " + " | ".join(headers) + " |\n"
markdown += "| " + " | ".join(["---"] * len(headers)) + " |\n"

for vaccine in ['Pfizer', 'Moderna']:
    row_values = [vaccine]
    total = 0
    for m in requested_months:
        val = results[vaccine][m]
        row_values.append(f"{val:,}")
        total += val
    row_values.append(f"{total:,}")
    markdown += "| " + " | ".join(row_values) + " |\n"

with open(r'C:\Users\aicil\.gemini\antigravity\scratch\covid_summary_ssa.md', 'w', encoding='utf-8') as f:
    f.write(markdown)

print("SUCCESS")
