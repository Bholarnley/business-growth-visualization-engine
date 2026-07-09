from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content("<h1 style='font-family:sans-serif'>BGVE says hello</h1>")
    page.screenshot(path="test_screenshot.png")
    browser.close()

print("Screenshot saved")