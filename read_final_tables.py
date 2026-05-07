import docx

file_path = r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\mezquital\INFORMES\Informe_Vacunacion_Mezquital_2026_Final_Heatmap.docx"

try:
    doc = docx.Document(file_path)
    for i, table in enumerate(doc.tables):
        print(f"\n--- Table {i} ---")
        for row in table.rows:
            print([cell.text.strip() for cell in row.cells])
except Exception as e:
    print(f"Error: {e}")
