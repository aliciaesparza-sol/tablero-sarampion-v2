import docx

file_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\INFORMES\Informe_Vacunacion_Mezquital_2026.05.05.2026.docx"

try:
    doc = docx.Document(file_path)
    print(f"Reading tables from {file_path}")
    for i, table in enumerate(doc.tables):
        if i >= 3: # My tables are likely 3, 4, etc. 0, 1, 2 are the 2025/2026 summaries.
            print(f"\n--- Table {i} ---")
            for row in table.rows[:10]: # First 10 rows
                print([cell.text.strip() for cell in row.cells])
except Exception as e:
    print(f"Error: {e}")
