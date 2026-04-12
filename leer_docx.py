import sys, zipfile, re, os, shutil

sys.stdout.reconfigure(encoding='utf-8')

docx_path = r'C:\Users\aicil\.gemini\antigravity\scratch\informe_sarampion.docx'
out_dir = r'C:\Users\aicil\.gemini\antigravity\scratch\docx_images'

# Extract images
if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
os.makedirs(out_dir)

with zipfile.ZipFile(docx_path, 'r') as z:
    namelist = z.namelist()
    print("Files in docx:")
    for n in namelist:
        print(n)
    
    # Extract media files
    for name in namelist:
        if name.startswith('word/media/'):
            z.extract(name, out_dir)
            print(f"Extracted: {name}")
    
    # Extract and print all text from document.xml
    with z.open('word/document.xml') as f:
        xml_content = f.read().decode('utf-8')
    
    # Extract all text nodes
    texts = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', xml_content)
    print("\n=== ALL TEXT FROM DOCUMENT ===")
    full_text = ' '.join(texts)
    print(full_text)
