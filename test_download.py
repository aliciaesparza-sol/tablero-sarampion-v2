import requests
import re
import warnings

warnings.filterwarnings('ignore')

session = requests.Session()

# Login
login_url = "https://siscensia.salud.gob.mx/sarampion_2025/ssa/login.php"
payload = {
    'user': 'E_DGO_ADMIN',
    'pass': 'QWERTY',
    'btn_login': 'Entrar'
}

print("Logging in...")
resp = session.post(login_url, data=payload, verify=False)
print("Status:", resp.status_code)
if 'sarampion_2025/ssa/index.php' in resp.url or 'reporte' in resp.text.lower():
    print("Login success!")

# The report URL from the previous browser session might be:
# https://siscensia.salud.gob.mx/sarampion_2025/ssa/reporte.php or similar.
# Since we need to download the CSV, let's see what the report page looks like.
report_url = "https://siscensia.salud.gob.mx/sarampion_2025/ssa/reporte.php"
resp2 = session.get(report_url, verify=False)
print("Report page size:", len(resp2.text))

# Let's see if we can trigger the CSV download
# Form inputs on the report page to generate the CSV:
csv_payload = {
    'tipo_reporte': 'sectorial',  # typical values based on UI
    'formato': 'csv',
    # other fields might be required depending on the HTML form
}
# We will just print the form inputs from the report page to figure out the exact POST request for the CSV.
inputs = re.findall(r'<input.*?name=[\'\"](.*?)[\'\"].*?>', resp2.text, re.IGNORECASE)
selects = re.findall(r'<select.*?name=[\'\"](.*?)[\'\"].*?>', resp2.text, re.IGNORECASE)
print("Report inputs:", inputs)
print("Report selects:", selects)
