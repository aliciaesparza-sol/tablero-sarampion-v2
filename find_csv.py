import os
import glob

possible_paths = [
    r"C:\Users\aicil\Downloads\*",
    r"C:\Users\aicil\OneDrive\Escritorio\*",
    r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\*",
    r"C:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\INFORME AUTOMATIZADO SARAMPION\*",
    r"C:\Descargas_SRP\*",
    r"C:\Users\aicil\.gemini\antigravity-ide\scratch\*"
]

found = False
for path in possible_paths:
    files = glob.glob(path)
    for f in files:
        if "30-06-2026" in f or "SRP-SR-2025" in f:
            print("Found:", f)
            found = True

if not found:
    print("No matching CSV file found in standard paths.")
