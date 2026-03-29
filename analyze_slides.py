import re

with open(r'C:\Users\aicil\.gemini\antigravity\scratch\measles_preview\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Unified regex to find slides and their first h2 or title-like element
slides = re.findall(r'<div class="[^"]*slide[^"]*".*?>(.*?)</div>\s*<!--', content, re.DOTALL)
# That didn't work well with nested divs. Let's use a simpler approach.

slide_blocks = content.split('<div class="slide')
print(f"Total slides found: {len(slide_blocks) - 1}")

for i, block in enumerate(slide_blocks):
    if i == 0: continue # Header/pre-content
    title_match = re.search(r'<h2>(.*?)</h2>', block, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "No Title"
    print(f"Slide {i-1}: {title}")
