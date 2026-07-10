from playwright.sync_api import sync_playwright
import os

here = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(here, "templates", "deadline_badge.html")
frames_dir = os.path.join(here, "frames_deadline_badge")
os.makedirs(frames_dir, exist_ok=True)

FPS = 30
DURATION = 4.0
TOTAL_FRAMES = int(FPS * DURATION)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1920})
    page.goto(f"file:///{html_path.replace(os.sep, '/')}")

    for i in range(TOTAL_FRAMES):
        page.screenshot(path=os.path.join(frames_dir, f"frame_{i:04d}.png"), omit_background=True)
        page.wait_for_timeout(1000 / FPS)

    browser.close()

print(f"Captured {TOTAL_FRAMES} frames into: {frames_dir}")