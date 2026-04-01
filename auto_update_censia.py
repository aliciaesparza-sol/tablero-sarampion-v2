from playwright.sync_api import sync_playwright
import os

def download_censia_data():
    output_path = "censia_latest.csv"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        try:
            print("Iniciando sesion en CeNSIA...")
            page.goto("https://siscensia.salud.gob.mx/sarampion_2025/", wait_until="domcontentloaded")
            page.fill("input[name='user']", "E_DGO_ADMIN")
            page.fill("input[name='pass']", "QWERTY")
            page.click("button[type='submit']")
            page.wait_for_load_state("domcontentloaded")
            page.goto("https://siscensia.salud.gob.mx/sarampion_2025/ssa/reporte.php", wait_until="domcontentloaded")
            print("Descargando CSV...")
            with page.expect_download(timeout=120000) as dl:
                page.click("button#descarga_todos")
            download = dl.value
            download.save_as(output_path)
            print(f"Descarga completada: {os.path.getsize(output_path):,} bytes")
        except Exception as e:
            print(f"Error durante el scraping: {e}")
            raise
        finally:
            browser.close()

if __name__ == "__main__":
    download_censia_data()
