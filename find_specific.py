import re

file_path = 'full_dump.txt'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

slides = content.split('--- SLIDE ')
for slide in slides[1:]:
    header_part = slide.split(' ---\n', 1)
    if len(header_part) < 2: continue
    index = header_part[0]
    body = header_part[1]
    
    first_line = body.strip().split('\n')[0] if body.strip() else "Empty"
    
    # Check for "DEFINICIÓN OPERACIONAL" or "CASO PROBABLE"
    if re.search(r'DEFINICI[OÓ]N OPERACIONAL|CASO PROBABLE|CASO CONFIRMADO|CASO DESCARTADO', body, re.IGNORECASE):
        print(f"Slide {index}: {first_line}")
