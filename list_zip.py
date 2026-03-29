import zipfile
import os

zip_path = r'c:\Users\aicil\OneDrive\Escritorio\PVU\IMSS BIENESTAR\ACUSES_VACUNACIÓN_2025_IMSS_BIENESTAR.zip'
try:
    with zipfile.ZipFile(zip_path, "r") as z:
        names = z.namelist()
        print(f"Total files in ZIP: {len(names)}")
        for name in names[:100]:
            print(name)
except Exception as e:
    print(f"Error: {e}")
