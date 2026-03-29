import re

filepath = r"C:\Users\aicil\.gemini\antigravity\scratch\Banco_Preguntas_Historia_Clinica.md"

with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# Remove the bold asterisks surrounding the question text
cleaned_text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(cleaned_text)

# Count how many questions there are by counting the number of ANSWER lines
count = text.count("ANSWER:")
print(f"Total questions: {count}")
