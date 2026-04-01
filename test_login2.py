import requests
import re
import warnings

warnings.filterwarnings('ignore')

url = "https://siscensia.salud.gob.mx/sarampion_2025/"
print("Fetching:", url)
try:
    text = requests.get(url, verify=False, timeout=10).text
    action = re.search(r'<form.*?action=[\'\"](.*?)[\'\"].*?>', text, re.IGNORECASE)
    if action:
        print("Action:", action.group(1))
    else:
        print("No form action found.")
    
    inputs = re.findall(r'<input.*?name=[\'\"](.*?)[\'\"].*?>', text, re.IGNORECASE)
    print("Inputs:", inputs)
except Exception as e:
    print("Error:", e)
