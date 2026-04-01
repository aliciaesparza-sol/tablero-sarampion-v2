from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    try:
        page.goto("https://siscensia.salud.gob.mx/sarampion_2025/", wait_until="domcontentloaded")
        page.fill("input[name='user']", "E_DGO_ADMIN")
        page.fill("input[name='pass']", "QWERTY")
        page.click("button, input[type='submit']")
        page.wait_for_load_state("domcontentloaded")
        
        page.goto("https://siscensia.salud.gob.mx/sarampion_2025/ssa/reporte.php", wait_until="domcontentloaded")
        
        with open("ui_elements.txt", "w", encoding="utf-8") as f:
            f.write("--- Selects ---\n")
            for x in page.query_selector_all("select"):
                opt = x.query_selector("option[selected]")
                f.write(f"Name: {x.get_attribute('name')} Selected: {opt.text_content() if opt else 'None'}\n")
                
            f.write("--- Buttons ---\n")
            for x in page.query_selector_all("button, input[type='button'], input[type='submit'], a.btn"):
                f.write(f"Text: {x.text_content().strip()} Value: {x.get_attribute('value')} ID: {x.get_attribute('id')} Class: {x.get_attribute('class')}\n")
            
    except Exception as e:
        print("Error:", e)
    finally:
        browser.close()
