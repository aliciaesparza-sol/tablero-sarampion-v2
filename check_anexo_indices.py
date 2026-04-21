import pandas as pd

def check_anexo_b_indices(path):
    df = pd.read_excel(path, sheet_name='ANEXO B', header=None)
    # Print row 4 and 5 with indices
    row4 = df.iloc[4].fillna('').tolist()
    row5 = df.iloc[5].fillna('').tolist()
    
    print("ANEXO B Row 4 Labels:")
    for i, label in enumerate(row4):
        print(f"{i}: {label}")
        
    print("\nANEXO B Row 5 Labels:")
    for i, label in enumerate(row5):
        print(f"{i}: {label}")

check_anexo_b_indices(r"c:\Users\aicil\OneDrive\Escritorio\PVU\SARAMPIÓN\FORMATOS\FORMATOS CENSIA\BLOQUEO VACUNAL\FORMATO RESPUESTA RAPIDA.xlsx")
