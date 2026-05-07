import pandas as pd

temp_excel = r"C:\Users\aicil\.gemini\antigravity\scratch\orig_temp.xlsx"

try:
    df = pd.read_excel(temp_excel, sheet_name="Concentrado", header=None)
    # Row 2 headers
    headers = df.iloc[2].tolist()
    print("Columns 54-61 headers:")
    for i in range(54, 62):
        print(f"Col {i}: {headers[i]}")
        
    # Check data for first locality
    print("\nData for first locality (AMOLES):")
    for i in range(len(df)):
        if "AMOLES" in str(df.iloc[i, 4]):
            print(df.iloc[i, [4] + list(range(54, 62))].tolist())
            break

except Exception as e:
    print(f"Error: {e}")
