import pandas as pd
import pypdf
import pdfplumber

def get_detailed_headers(path, sheet_name):
    print(f"--- Detailed Headers for: {path} [{sheet_name}] ---")
    df = pd.read_excel(path, sheet_name=sheet_name, header=None)
    # Fill NaNs with empty string for better visibility
    df = df.fillna('')
    # Print the first 20 rows to locate headers
    print(df.head(20).to_string())

def extract_pdf_content(path):
    print(f"--- Extracting PDF: {path} ---")
    try:
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages):
                print(f"--- Page {i+1} Text ---")
                print(page.extract_text())
                print(f"--- Page {i+1} Tables ---")
                tables = page.extract_tables()
                for j, table in enumerate(tables):
                    print(f"Table {j+1}:")
                    for row in table:
                        print(row)
    except Exception as e:
        print(f"Error extracting PDF: {e}")

get_detailed_headers(r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\FORMATOS\FORMATOS CENSIA\BLOQUEO VACUNAL\FORMATO RESPUESTA RAPIDA.xlsx", "ANEXO B")
extract_pdf_content(r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\Informe_Vacunacion_Mezquital_2026.15.04.2026.pdf")
