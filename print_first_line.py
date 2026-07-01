import os
BASE_DIR = r"C:\Users\aicil\.gemini\antigravity-ide\scratch"
csv_path = os.path.join(BASE_DIR, "SRP-SR-2025_02-04-2026 10-40-30.csv")

with open(csv_path, 'r', encoding='latin1') as f:
    for i in range(3):
        print(f"Line {i}:", repr(f.readline()))
