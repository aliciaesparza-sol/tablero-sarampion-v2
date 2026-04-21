import docx
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

# Load existing template
doc = docx.Document(r"c:\Users\aicil\OneDrive\Escritorio\hoja MEMBRETADA GIGANTE2026_carta.docx")

def add_header_paragraph(text, bold=False, align=WD_PARAGRAPH_ALIGNMENT.CENTER, size=12):
    p = doc.add_paragraph()
    p.alignment = align
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = 'Arial'

add_header_paragraph("INFORME DE DOSIS APLICADAS EN EL MUNICIPIO DE EL MEZQUITAL", bold=True, size=14)
add_header_paragraph("CAMPAÑA DE VACUNACIÓN 2025 - 2026\n", bold=False, size=12)

def set_table_header_bg_color(cell, color):
    try:
        shading_elm = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), color))
        cell._tc.get_or_add_tcPr().append(shading_elm)
    except:
        pass

def create_dosis_table(title, data, headers):
    p = doc.add_paragraph()
    run = p.add_run(title)
    run.bold = True
    run.font.size = Pt(11)
    
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        hdr_cells[i].text = header
        if len(hdr_cells[i].paragraphs[0].runs) > 0:
            hdr_cells[i].paragraphs[0].runs[0].bold = True
        set_table_header_bg_color(hdr_cells[i], "D9D9D9")
        
    for row_data in data:
        row_cells = table.add_row().cells
        for i, item in enumerate(row_data):
            row_cells[i].text = str(item)
            if i == 0 or "TOTAL" in str(item).upper():
                if len(row_cells[i].paragraphs[0].runs) > 0:
                    row_cells[i].paragraphs[0].runs[0].bold = True

    p_source = doc.add_paragraph()
    run_s = p_source.add_run("Fuente: SIS/CeNSIA, consultado el 15 de abril de 2026; 18:00 hs.")
    run_s.italic = True
    run_s.font.size = Pt(9)
    p_source.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    doc.add_paragraph()

headers_dosis = ["Valores", "IMSS B", "SSA", "Suma total"]

# Table 1: 2025
data_2025 = [
    ["SRP PRIMERA TOTAL", 587, 1043, 1630],
    ["SRP SEGUNDA TOTAL", 1526, 1255, 2781],
    ["SR PRIMERA TOTAL", 495, 645, 1140],
    ["SR SEGUNDA TOTAL", 704, 254, 958],
    ["TOTAL", 3312, 3197, 6509]
]
create_dosis_table("DOSIS APLICADAS EN EL MUNICIPIO DE EL MEZQUITAL, DURANGO DURANTE 2025", data_2025, headers_dosis)

# Table 2: 2026
data_2026 = [
    ["SRP PRIMERA TOTAL", 91, 1842, 1933],
    ["SRP SEGUNDA TOTAL", 229, 5163, 5392],
    ["SR PRIMERA TOTAL", 273, 657, 930],
    ["SR SEGUNDA TOTAL", 205, 1129, 1334],
    ["TOTAL", 798, 8791, 9589]
]
create_dosis_table("DOSIS APLICADAS EN EL MUNICIPIO DE EL MEZQUITAL, DURANGO DURANTE 2026", data_2026, headers_dosis)

# Table 3: 2025-2026
data_2526 = [
    ["SRP PRIMERA TOTAL", 678, 2885, 3563],
    ["SRP SEGUNDA TOTAL", 1755, 6418, 8173],
    ["SR PRIMERA TOTAL", 768, 1302, 2070],
    ["SR SEGUNDA TOTAL", 909, 1383, 2292],
    ["TOTAL", 4110, 11988, 16098]
]
create_dosis_table("DOSIS APLICADAS EN EL MUNICIPIO DE EL MEZQUITAL, DURANGO DURANTE 2025 Y 2026", data_2526, headers_dosis)

# Table 4: Dates and bases
headers_dates = ["Fecha(s)", "Localidad / Base", "SRP", "SR", "Total"]
data_dates = [
    ["29 Ene", "La Guajolota (Las Agulillas)", 105, 327, 432],
    ["30 Ene", "La Guajolota (Bajío y Centro)", 175, 228, 403],
    ["03 Feb", "Cerro Bolillo, Sta. Ma. de Ocotán", 150, 445, 595],
    ["11 Feb", "Luis Moya (Gpe. Victoria)", "2", 151, 153],
    ["12 Feb", "Luis Moya (Gpe. Victoria)", "2", 164, 166],
    ["24 Feb", "Cerro Bolillo, Sta. Ma. de Ocotán", 120, 358, 478],
    ["01 Mar", "Las Joyas, Mezquital", 124, 483, 607],
    ["26 Mar", "La Huazamotita", "0", 307, 307],
    ["27 Mar", "La Huazamotita", "0", 281, 281],
    ["28 Mar", "Las Joyas, Mezquital", 95, 693, 788],
    ["TOTAL", "", 773, "3,647", "4,420"]
]

p4 = doc.add_paragraph()
run4 = p4.add_run("DETALLE DE DOSIS APLICADAS POR LOCALIDAD / BASE")
run4.bold = True
run4.font.size = Pt(11)

t4 = doc.add_table(rows=1, cols=len(headers_dates))
t4.style = 'Table Grid'
hdr_cells4 = t4.rows[0].cells
for i, header in enumerate(headers_dates):
    hdr_cells4[i].text = header
    if len(hdr_cells4[i].paragraphs[0].runs) > 0:
        hdr_cells4[i].paragraphs[0].runs[0].bold = True
    set_table_header_bg_color(hdr_cells4[i], "D9D9D9")

for row_data in data_dates:
    row_cells = t4.add_row().cells
    for i, item in enumerate(row_data):
        row_cells[i].text = str(item)
        if "TOTAL" in str(item).upper():
            if len(row_cells[i].paragraphs[0].runs) > 0:
                row_cells[i].paragraphs[0].runs[0].bold = True

out_path = r"c:\Users\aicil\OneDrive\Escritorio\Informe_Vacunacion_Mezquital_2026.docx"
doc.save(out_path)
print("Saved to", out_path)
