import zipfile
import pdfplumber
import io

zip_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\CASOS NOTIFICADOS\CASOS NOTIFICADOS 2026\EE casos confirmados sarampion 2026-20260303T152644Z-1-001.zip"
sample_files = ['1. 48157 GRRH.pdf', '10. 50555 FCCR.pdf']

with zipfile.ZipFile(zip_path, 'r') as z:
    with open('poc_out.txt', 'w', encoding='utf-8') as out_file:
        for file_name in sample_files:
            out_file.write(f"--- START OF {file_name} ---\n")
            try:
                # Extraemos el PDF a memoria
                pdf_bytes = z.read(file_name)
                with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                    for i, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text:
                            out_file.write(f"--- PAGE {i+1} ---\n")
                            out_file.write(text + "\n")
            except Exception as e:
                out_file.write(f"Error reading {file_name}: {e}\n")
            out_file.write(f"--- END OF {file_name} ---\n\n")

print("POC extraction complete. Check poc_out.txt")
