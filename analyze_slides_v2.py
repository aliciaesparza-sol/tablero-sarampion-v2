import re

with open(r'C:\Users\aicil\.gemini\antigravity\scratch\measles_preview\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all blocks starting with <div class="slide
# We'll use a regex that matches the start of a slide div and captures until the next one or the end
slide_blocks = re.split(r'<div\s+(?:id="[^"]*"\s+)?class="slide', content)[1:]

print(f"Total slides found: {len(slide_blocks)}")

for i, block in enumerate(slide_blocks):
    # Search for h2 title in this block
    title_match = re.search(r'<h2>(.*?)</h2>', block, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "No h2 Title"
    # Special check for Slide 1 (Portada) which might not have h2
    if i == 0 and "Sarampión" in block:
        title = "PORTADA"
    
    print(f"Slide {i}: {title}")
