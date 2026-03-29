import re
import sys
import io

# Ensure UTF-8 output for terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\aicil\.gemini\antigravity\scratch\measles_preview\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Splitting by the start of a slide div
# This handles both <div class="slide"> and <div id="..." class="slide ...">
slide_starts = list(re.finditer(r'<div\s+(?:id="[^"]*"\s+)?class=["\']slide', content))

print(f"Total slides: {len(slide_starts)}")
for i, match in enumerate(slide_starts):
    start = match.start()
    end = slide_starts[i+1].start() if i+1 < len(slide_starts) else len(content)
    chunk = content[start:end]
    
    h2_match = re.search(r'<h2>(.*?)</h2>', chunk, re.DOTALL)
    title = h2_match.group(1).strip() if h2_match else "No h2 Title"
    
    # Catch Portada specifically
    if "Sarampión" in chunk and i == 0:
        title = "PORTADA"
    
    print(f"Index {i}: {title}")
