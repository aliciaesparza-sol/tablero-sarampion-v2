import re

filepath = r"C:\Users\aicil\.gemini\antigravity\scratch\Banco_Preguntas_Historia_Clinica.md"

with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# Remove the title
text = re.sub(r'^# BANCO DE PREGUNTAS: HISTORIA CLÍNICA PEDIÁTRICA\n+', '', text)

# Remove the question numbers (e.g., '1. ', '2. ', etc.) at the beginning of lines
text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Removed title and numbering successfully.")
