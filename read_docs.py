import docx
import os

def read_docx(file_path):
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

model_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\CAMPAÑA DE VACUNACION MASIVA INTERINSTITUCIONAL DICIEMBRE 2025\MACROCENTROS UNIVERSITARIOS 25 MARZO 2026\FICHA TECNICA MACROCENTROS DE VACUNACIÓN UNIVERSITARIOS 25 MARZO 2026.docx"
letterhead_path = r"c:\Users\aicil\OneDrive\Escritorio\hoja MEMBRETADA GIGANTE2026_carta.docx"

print("--- MODEL CONTENT ---")
print(read_docx(model_path))
print("\n--- LETTERHEAD CONTENT ---")
print(read_docx(letterhead_path))
