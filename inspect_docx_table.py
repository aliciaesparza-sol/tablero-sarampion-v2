from docx import Document
import os

path = 'mezquital_card.docx'
if os.path.exists(path):
    doc = Document(path)
    for i, table in enumerate(doc.tables):
        print(f"Table {i}:")
        for r_idx, row in enumerate(table.rows):
            cells = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
            print(f"  Row {r_idx}: {cells}")
else:
    print(f"File not found: {path}")
