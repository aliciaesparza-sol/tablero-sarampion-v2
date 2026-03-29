import os
import glob

path = r"C:\Users\aicil\.gemini\antigravity\scratch"
files = os.listdir(path)
print("Files in scratch:")
for f in files:
    if f.endswith(".pptx"):
        print(f"FOUND PPTX: {f}")
    if "sarampion" in f.lower():
        print(f"FOUND POTENTIAL: {f}")

full_path = os.path.join(path, "sarampion_pres.pptx")
print(f"Checking full path: {full_path}")
print(f"Exists: {os.path.exists(full_path)}")
