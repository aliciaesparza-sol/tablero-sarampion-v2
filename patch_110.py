import re

with open(r'C:\Users\aicil\.gemini\antigravity\scratch\generar_informe.py', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('60 brigadas activas', '110 brigadas activas'),
    ('"60 brigadas"', '"110 brigadas"'),
    ('"60"', '"110"'),
    ('60 brigadas', '110 brigadas'),
    ('97 dosis/brigada/dia', '53 dosis/brigada/dia'),
    ('97 dosis', '53 dosis'),
    ('188 dosis/brigada/dia', '102 dosis/brigada/dia'),
    ('188 dosis', '102 dosis'),
    ('124 dosis/brigada/dia', '68 dosis/brigada/dia'),
    ('Informe_Ejecutivo_Sarampion_10-04-2026.docx', 'Informe_Ejecutivo_Sarampion_110brigadas_10-04-2026.docx'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(r'C:\Users\aicil\.gemini\antigravity\scratch\generar_informe_110.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Archivo creado OK")
