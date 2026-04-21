from pptx import Presentation

TEMPLATE_PATH = r"c:\Users\aicil\OneDrive\Escritorio\plantilla presentacion ppt.pptx"
try:
    prs = Presentation(TEMPLATE_PATH)
    print(f"La plantilla tiene {len(prs.slide_layouts)} diseños de diapositiva:")
    for i, layout in enumerate(prs.slide_layouts):
        print(f"{i}: {layout.name}")
except Exception as e:
    print(f"Error al abrir la plantilla: {e}")
