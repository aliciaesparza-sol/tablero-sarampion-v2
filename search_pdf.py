import fitz # PyMuPDF
import re

pdf_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\POBLACIÓN\POBLACION CONAPO.pdf'
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")

keywords = ["meses", "18", "6-11", "6 a 11", "etario"]

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    for kw in keywords:
        if re.search(re.escape(kw), text, re.IGNORECASE):
            print(f"Page {page_num + 1} matches keyword '{kw}'")
            # Print page text snippet
            lines = text.split('\n')
            for line in lines:
                if kw.lower() in line.lower():
                    print(f"  Line: {line.strip()}")
