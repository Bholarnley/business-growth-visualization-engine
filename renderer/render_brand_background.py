from playwright.sync_api import sync_playwright
import os

here = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(here, "templates", "brand_background.html")
output_path = os.path.join(here, "brand_background.png")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1920})
    page.goto(f"file:///{html_path.replace(os.sep, '/')}")
    page.wait_for_timeout(300)
    page.screenshot(path=output_path)  # no omit_background - we WANT this one solid/opaque
    browser.close()

print(f"Brand background saved to: {output_path}")