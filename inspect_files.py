import fitz # PyMuPDF
import sys
from pptx import Presentation
import os

pdf_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\LINEAMIENTOS\Docto_PlanSarampion_10abr2020.pdf"
pptx_path = r"c:\Users\aicil\OneDrive\Escritorio\plantilla presentacion ppt.pptx"

def inspect_pptx():
    print(f"Inspecting PPTX: {pptx_path}")
    if not os.path.exists(pptx_path):
        print("PPTX not found!")
        return

    prd = Presentation(pptx_path)
    print(f"Number of layouts: {len(prd.slide_layouts)}")
    for i, layout in enumerate(prd.slide_layouts):
        print(f"Layout {i} - {layout.name}")
        for ph in layout.placeholders:
            print(f"  Placeholder: {ph.placeholder_format.idx} (type: {ph.placeholder_format.type}) name: {ph.name}")

def extract_pdf():
    print(f"Extracting PDF: {pdf_path}")
    if not os.path.exists(pdf_path):
        print("PDF not found!")
        return
        
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += f"\\n--- PAGE {page_num + 1} ---\\n"
        text += page.get_text("text")
        
    with open("pdf_extracted.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extraction complete, {len(doc)} pages.")

if __name__ == '__main__':
    inspect_pptx()
    extract_pdf()
