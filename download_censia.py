import os
import sys
import time
from playwright.sync_api import sync_playwright

CENSIA_URL = "https://siscensia.salud.gob.mx/sarampion_2025/"
CENSIA_USER = "E_DGO_ADMIN"
CENSIA_PASS = "QWERTY"
output_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "censia_descarga_hoy.csv")

def attempt_download():
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        
        # Enable console log forwarding
        page.on("console", lambda msg: print(f"Browser Log: {msg.text}"))
        
        print("Navigating to CENSIA login page...")
        page.goto(CENSIA_URL, wait_until="domcontentloaded", timeout=45000)
        print("Loaded login page. URL:", page.url)
        
        # Check if already logged in (unlikely but possible if session persists somehow, though we are in a new context)
        try:
            print("Filling login credentials...")
            page.fill("input[name='user']", CENSIA_USER, timeout=15000)
            page.fill("input[name='pass']", CENSIA_PASS)
            print("Clicking login submit...")
            page.click("button[type='submit']")
            page.wait_for_load_state("domcontentloaded", timeout=15000)
            print("Login submitted.")
        except Exception as e:
            print("Login fill/submit failed or skipped (might be already on report page):", e)
            
        print("Navigating to report page...")
        page.goto("https://siscensia.salud.gob.mx/sarampion_2025/ssa/reporte.php", wait_until="domcontentloaded", timeout=45000)
        print("Report page loaded. URL:", page.url)
        
        print("Waiting for download button to be visible...")
        # Wait for the download button to be on the page
        page.wait_for_selector("button#descarga_todos, a#descarga_todos", timeout=15000)
        
        print("Clicking download button...")
        with page.expect_download(timeout=180000) as dl:
            clicked = False
            for sel in ["button#descarga_todos", "a#descarga_todos", "button:has-text('Descargar')", "a:has-text('CSV')"]:
                try:
                    el = page.query_selector(sel)
                    if el:
                        print(f"Clicking selector '{sel}'...")
                        el.click()
                        clicked = True
                        break
                except Exception as e:
                    print(f"Selector '{sel}' failed: {e}")
                    
            if not clicked:
                raise Exception("Could not find download button on page")
                
        print("Downloading file...")
        dl.value.save_as(output_csv)
        print(f"File downloaded successfully to {output_csv}!")
        print("File size:", os.path.getsize(output_csv), "bytes")
        browser.close()
        return True

max_retries = 3
success = False
for attempt in range(1, max_retries + 1):
    print(f"\n--- Attempt {attempt} of {max_retries} ---")
    try:
        if attempt_download():
            success = True
            break
    except Exception as e:
        print(f"Attempt {attempt} failed: {e}")
        if attempt < max_retries:
            print("Waiting 10 seconds before next attempt...")
            time.sleep(10)

if not success:
    print("Failed to download file after all attempts.")
    sys.exit(1)
else:
    print("Download completed successfully!")
    sys.exit(0)
