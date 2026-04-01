from playwright.sync_api import sync_playwright
import os

def download_censia_data():
    output_path = "censia_latest.csv"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("Iniciando sesion en CeNSIA...")
            page.goto("https://siscensia.salud.gob.mx/sarampion_2025/", wait_until="domcontentloaded")
            page.fill("input[name='user']", "E_DGO_ADMIN")
            page.fill("input[name='pass']", "QWERTY")
            page.click("button, input[type='submit']")
            page.wait_for_load_state("domcontentloaded")
            
            print("Navegando a reportes...")
            page.goto("https://siscensia.salud.gob.mx/sarampion_2025/ssa/reporte.php", wait_until="domcontentloaded")
            
            print("Solicitando descarga de CSV (puede tardar unos segundos)...")
            with page.expect_download(timeout=60000) as download_info:
                # El id descarga_todos parece ser el boton de exportar CSV completo
                page.click("button#descarga_todos")
            
            download = download_info.value
            download.save_as(output_path)
            print(f"Descarga completada con exito en: {output_path}")
            
        except Exception as e:
            print(f"Error durante el scraping: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    download_censia_data()
