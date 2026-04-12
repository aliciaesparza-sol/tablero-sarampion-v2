import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_table_border(table):
    """Adds a simple black border to the table."""
    tbl = table._tbl
    for row in tbl.tr_lst:
        for cell in row.tc_lst:
            tcPr = cell.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')
            top = OxmlElement('w:top')
            top.set(qn('w:val'), 'single')
            top.set(qn('w:sz'), '4')
            top.set(qn('w:space'), '0')
            top.set(qn('w:color'), '000000')
            tcBorders.append(top)
            bottom = OxmlElement('w:bottom')
            bottom.set(qn('w:val'), 'single')
            bottom.set(qn('w:sz'), '4')
            bottom.set(qn('w:space'), '0')
            bottom.set(qn('w:color'), '000000')
            tcBorders.append(bottom)
            left = OxmlElement('w:left')
            left.set(qn('w:val'), 'single')
            left.set(qn('w:sz'), '4')
            left.set(qn('w:space'), '0')
            left.set(qn('w:color'), '000000')
            tcBorders.append(left)
            right = OxmlElement('w:right')
            right.set(qn('w:val'), 'single')
            right.set(qn('w:sz'), '4')
            right.set(qn('w:space'), '0')
            right.set(qn('w:color'), '000000')
            tcBorders.append(right)
            tcPr.append(tcBorders)

def generate_report():
    doc = docx.Document()
    
    # Title
    title = doc.add_heading('INFORME DE GOBIERNO 2025: AVANCE EN MATERIA DE VACUNACIÓN', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.color.rgb = docx.shared.RGBColor(0, 0, 0)
        run.font.name = 'Arial'

    # Content
    paragraphs = [
        "2025 se consolida como un periodo clave en el fortalecimiento del sistema de salud pública, logrando avances históricos en las coberturas de vacunación durante el trimestre de octubre a diciembre en comparación con el mismo ciclo del año anterior.",
        "2025 destaca por la excelente gestión operativa en la aplicación de la vacuna SRP (Sarampión, Rubéola y Parotiditis), donde se alcanzó una cobertura del 91% en primera dosis con 3,467 aplicaciones, superando considerablemente las 3,005 dosis (67%) registradas en el 2024.",
        "2025 refuerza la inmunización infantil con un avance del 72% en la segunda dosis de SRP (2,746 dosis), lo que representa un crecimiento significativo frente al 50% logrado en el periodo homólogo de 2024, asegurando esquemas completos en la población objetivo.",
        "2025 reporta un éxito sin precedentes en la campaña de vacunación contra el Virus del Papiloma Humano (VPH), alcanzando 38,705 dosis aplicadas para una cobertura sectorial del 92%, superando de manera contundente el 78% alcanzado en la campaña del año previo.",
        "2025 evidencia una respuesta masiva y eficiente en la inmunización contra la Influenza Estacional, logrando proteger a 338,300 ciudadanos (71% de avance meta), una cifra que supera por gran margen los 280,100 protegidos (60%) del ciclo 2024.",
        "2025 demuestra un compromiso firme en la prevención del COVID-19 con la aplicación de 56,211 dosis (84% de la meta), lo que significa una mejora sustancial y un incremento en la aceptación social respecto a las 26,510 dosis (65%) del año anterior.",
        "2025 garantiza el bienestar de la población infantil mediante la vacuna Hexavalente, logrando aplicar 3,322 dosis que equivalen al 85% de la meta institucional, superando la eficiencia del 75% observada en el mismo trimestre del 2024.",
        "2025 proyecta el éxito de las brigadas de salud en la aplicación de biológicos esenciales como Rotavirus y Neumocócica, alcanzando coberturas del 83% y 84% respectivamente, superando en ambos casos el desempeño logístico del año fiscal anterior.",
        "2025 asegura la continuidad de los servicios de inmunización a través de una red de distribución fortalecida, garantizando que el derecho a la salud se traduzca en hechos concretos y metas superadas para beneficio de todas las familias duranguenses."
    ]

    for p_text in paragraphs:
        p = doc.add_paragraph(p_text)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Arial'
        font.size = Pt(11)

    # Tables
    doc.add_heading('Comparativa de Avances en Vacunación (Octubre - Diciembre)', 2).runs[0].font.color.rgb = docx.shared.RGBColor(0, 0, 0)
    
    table_data = [
        ["Biología / Vacuna", "Estado 2024 (Avance %)", "Estado 2025 (Avance %)", "Mejora / Observación"],
        ["SRP (1ª Dosis)", "3,005 (67%)", "3,467 (91%)", "+24% Cobertura"],
        ["SRP (2ª Dosis)", "2,245 (50%)", "2,746 (72%)", "+22% Cobertura"],
        ["VPH (Campaña)", "32,150 (78%)", "38,705 (92%)", "+14% Alcance"],
        ["Influenza Estacional", "280,100 (60%)", "338,300 (71%)", "+58,200 Dosis"],
        ["COVID-19 (Invernal)", "26,510 (65%)", "56,211 (84%)", "+29,701 Dosis"],
        ["Hexavalente", "2,905 (75%)", "3,322 (85%)", "+10% Logística"],
        ["Rotavirus", "2,850 (76%)", "3,150 (83%)", "+7% Avance"],
        ["Neumocócica 13v", "2,920 (76%)", "3,280 (84%)", "+8% Cobertura"]
    ]

    table = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
    table.style = 'Table Grid'
    
    for r_idx, row in enumerate(table_data):
        for c_idx, text in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = text
            # Format text in cell
            para = cell.paragraphs[0]
            if not para.runs:
                para.add_run(text)
            run = para.runs[0]
            run.font.name = 'Arial'
            run.font.size = Pt(10)
            if r_idx == 0:
                run.bold = True
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    set_table_border(table)

    output_path = r"c:\Users\aicil\OneDrive\Escritorio\PVU\INFORMES PVU\INFORME DE GOBIERNO\INFORME DE GOBIERNO 2025\INFORME_GOBIERNO_2025_VACUNACION_MEJORADO.docx"
    doc.save(output_path)
    print(f"Report generated at: {output_path}")

if __name__ == "__main__":
    generate_report()
