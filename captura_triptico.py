from playwright.sync_api import sync_playwright
import os

html_path = os.path.abspath("triptico.html")
output_path = os.path.abspath("triptico_VPH.png")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1400, "height": 800})
    page.goto(f"file:///{html_path}")
    page.wait_for_timeout(3000)
    # Captura solo el elemento brochure-container
    element = page.query_selector(".brochure-container")
    if element:
        element.screenshot(path=output_path)
    else:
        page.screenshot(path=output_path, full_page=True)
    browser.close()

print(f"Guardado en: {output_path}")
