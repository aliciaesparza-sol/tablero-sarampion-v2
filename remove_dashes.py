import re

filepath = r"C:\Users\aicil\.gemini\antigravity\scratch\Banco_Preguntas_Historia_Clinica.md"

with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# Remove the '---' separators
cleaned_text = re.sub(r'\n---\n', '\n', text)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(cleaned_text)

print(f"Removed dashes successfully.")
