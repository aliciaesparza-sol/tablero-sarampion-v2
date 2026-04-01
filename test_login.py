import requests

login_url = "https://siscensia.salud.gob.mx/sarampion_2025/ssa/login.php"
payload = {
    'usuario': 'E_DGO_ADMIN',
    'pass': 'QWERTY',
    'btn_login': 'INGRESAR'
}

session = requests.Session()
# Intentar login
resp = session.post(login_url, data=payload, verify=False)
print("Status:", resp.status_code)
# Comprobar si redirigió a index o guardó cookies
print("Cookies:", session.cookies.get_dict())
if 'index.php' in resp.url or 'reporte' in resp.text.lower():
    print("Login aparentemente exitoso.")
else:
    print("Posible fallo en login.")
