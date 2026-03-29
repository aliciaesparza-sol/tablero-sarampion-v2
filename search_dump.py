import re

file_path = 'full_dump.txt'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

slides = content.split('--- SLIDE ')
for slide in slides[1:]: # Skip the first empty part
    header = slide.split(' ---')[0]
    body = slide.split(' ---')[1]
    
    if re.search(r'CASO|DEFINIC|OPERACIONAL|PROBABLE|CONFIRMADO', body, re.IGNORECASE):
        print(f"Match Slide {header}:")
        print(body.strip()[:300]) # Print first 300 chars
        print("-" * 30)
