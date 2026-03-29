import os

search_text = "Definición Operacional de Caso"
root_dirs = [
    r"C:\Users\aicil\.gemini\antigravity\scratch\ESTRATEGIA-SARAMPI-N-2026-main",
    r"C:\Users\aicil\.gemini\antigravity\scratch\measles-presentation",
    r"C:\Users\aicil\.gemini\antigravity\scratch\measles_presentation",
    r"C:\Users\aicil\.gemini\antigravity\scratch\measles_preview"
]

for root_dir in root_dirs:
    if not os.path.exists(root_dir):
        continue
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith((".html", ".js", ".json")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        if search_text in f.read():
                            print(f"FOUND in: {path}")
                except:
                    pass
