
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from docx import Document

doc = Document(r'C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\CONASABI\EVIDENCIAS CONASABI_24ABRIL2026\DSP_Vacunación_CONASABIAc2_24abril2026_ACTUALIZADO.docx')

print("=== TODOS LOS PÁRRAFOS CON TEXTO ===")
for i, p in enumerate(doc.paragraphs):
    if p.text.strip():
        print(f"[{i}] {p.text[:250]}")
