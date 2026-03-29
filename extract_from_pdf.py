import pdfplumber

pdf_path = r'c:\Users\aicil\.gemini\antigravity\scratch\Presentacion_COEVA_Sarampion_Durango_2026.pdf'

try:
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                print(f"\n--- PAGE {i} ---")
                print(text)
                all_text += f"\n--- PAGE {i} ---\n{text}"
        
        with open('extracted_pdf_text.txt', 'w', encoding='utf-8') as f:
            f.write(all_text)
except Exception as e:
    print(f"Error: {e}")
