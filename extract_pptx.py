import sys
import os
from pptx import Presentation
import json

def extract_pptx_content(pptx_path, output_file):
    if not os.path.exists(pptx_path):
        return f"Error: File not found at {pptx_path}"

    try:
        prs = Presentation(pptx_path)
    except Exception as e:
        return f"Error opening PPTX: {str(e)}"

    content = []

    for i, slide in enumerate(prs.slides):
        slide_title = ""
        if slide.shapes.title:
            slide_title = slide.shapes.title.text
        
        slide_text = []
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text:
                if shape.text.strip() and shape.text != slide_title:
                    slide_text.append(shape.text.strip())
        
        # Check for images and notes
        images_count = sum(1 for shape in slide.shapes if shape.shape_type == 13)
        notes = ""
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text

        content.append({
            "slide_index": i + 1,
            "title": slide_title,
            "text": slide_text,
            "images_count": images_count,
            "notes": notes
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)
    
    return f"Successfully extracted {len(content)} slides to {output_file}"

if __name__ == "__main__":
    pptx_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\COEVA\PRESENTACIONES\CAPACITACIÓN SARAMPIÓN CLÍNICA Y VACUNACIÓN 17FEBRERO 2026.pptx'
    output_path = r"C:\Users\aicil\.gemini\antigravity\scratch\extracted_ppt_data.json"
    result = extract_pptx_content(pptx_path, output_path)
    print(result)
