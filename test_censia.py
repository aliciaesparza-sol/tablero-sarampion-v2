import os
from playwright.sync_api import sync_playwright

CENSIA_URL = "https://siscensia.salud.gob.mx/sarampion_2025/"
CENSIA_USER = "E_DGO_ADMIN"
CENSIA_PASS = "QWERTY"

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        print("Navigating to CENSIA...")
        page.goto(CENSIA_URL, wait_until="networkidle", timeout=30000)
        print("Page title:", page.title())
        print("Page URL:", page.url)
        
        # Take screenshot to see what's on the page
        page.screenshot(path="censia_login.png")
        print("Screenshot saved to censia_login.png")
        
        # Let's inspect input elements
        inputs = page.query_selector_all("input")
        print(f"Found {len(inputs)} inputs:")
        for inp in inputs:
            print("  Name:", inp.get_attribute("name"), "Type:", inp.get_attribute("type"), "Id:", inp.get_attribute("id"))
            
        browser.close()
except Exception as e:
    print("Error:", e)
