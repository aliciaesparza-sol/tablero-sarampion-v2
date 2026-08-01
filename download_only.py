import os
from playwright.sync_api import sync_playwright

CENSIA_URL = "https://siscensia.salud.gob.mx/sarampion_2025/"
CENSIA_USER = "E_DGO_ADMIN"
CENSIA_PASS = "QWERTY"
output_csv = "censia_test_download.csv"

try:
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        
        print("Navigating to CENSIA URL...")
        page.goto(CENSIA_URL, wait_until="networkidle", timeout=60000)
        print("Loaded login page. URL:", page.url)
        
        print("Filling login fields...")
        page.fill("input[name='user']", CENSIA_USER, timeout=10000)
        page.fill("input[name='pass']", CENSIA_PASS)
        print("Clicking submit...")
        page.click("button[type='submit']")
        
        print("Waiting for page load after login...")
        page.wait_for_load_state("networkidle", timeout=30000)
        print("Logged in. Current URL:", page.url)
        
        print("Navigating to report page...")
        page.goto("https://siscensia.salud.gob.mx/sarampion_2025/ssa/reporte.php", wait_until="networkidle", timeout=60000)
        print("Report page loaded. URL:", page.url)
        
        page.screenshot(path="censia_report.png")
        print("Screenshot of report page saved to censia_report.png")
        
        print("Locating download buttons...")
        # Check download buttons on the page
        buttons = page.query_selector_all("button, a")
        for btn in buttons:
            text = btn.inner_text()
            btn_id = btn.get_attribute("id")
            if text or btn_id:
                print(f"  Element - ID: {btn_id}, Text: '{text}', Tag: {btn.evaluate('el => el.tagName')}")
        
        print("Attempting to click download button...")
        with page.expect_download(timeout=180000) as dl:
            clicked = False
            for sel in ["button#descarga_todos", "a#descarga_todos", "button:has-text('Descargar')", "a:has-text('CSV')"]:
                try:
                    el = page.query_selector(sel)
                    if el:
                        print(f"Found element with selector '{sel}'. Clicking...")
                        el.click()
                        clicked = True
                        break
                except Exception as e:
                    print(f"Failed click on '{sel}': {e}")
                    continue
            if not clicked:
                print("Could not find download button with standard selectors. Let's look for any button/link with 'descarga' or similar.")
                for btn in buttons:
                    btn_id = btn.get_attribute("id")
                    if btn_id and "descarga" in btn_id.lower():
                        print(f"Clicking custom element with ID '{btn_id}'...")
                        btn.click()
                        clicked = True
                        break
        
        print("Saving download...")
        dl.value.save_as(output_csv)
        print(f"Download saved successfully to {output_csv}!")
        print("File size:", os.path.getsize(output_csv), "bytes")
        browser.close()
except Exception as e:
    print("Error during download process:", e)
