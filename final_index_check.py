import re
import sys
import io

# Ensure UTF-8 output for terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\aicil\.gemini\antigravity\scratch\measles_preview\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all blocks starting with class="slide or class='slide or id="..." class="slide
# Using a more robust regex for the slide container
slide_matches = re.finditer(r'<div\s+[^>]*?class=["\']slide\b', content)

for i, match in enumerate(slide_matches):
    start_pos = match.start()
    # Find the next slide or the end of the presentation container
    next_match = re.search(r'<div\s+[^>]*?class=["\']slide\b', content[start_pos + 1:])
    end_pos = start_pos + 1 + next_match.start() if next_match else len(content)
    
    slide_content = content[start_pos:end_pos]
    h2_match = re.search(r'<h2>(.*?)</h2>', slide_content, re.DOTALL)
    title = h2_match.group(1).strip() if h2_match else "PORTADA (No h2)"
    print(f"Index {i}: {title}")
