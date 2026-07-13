from playwright.sync_api import sync_playwright
import os
import sys
import re

here = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(here, "templates", "warning_shake.html")

FPS = 30
DURATION = 3.0
TOTAL_FRAMES = int(FPS * DURATION)


def slugify(text, max_len=30):
    slug = re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')
    return slug[:max_len]


def render_warning(label_text):
    slug = slugify(label_text)
    frames_dir = os.path.join(here, f"frames_warning_{slug}")
    os.makedirs(frames_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(f"file:///{html_path.replace(os.sep, '/')}")

        page.evaluate(f'document.getElementById("warnLabel").textContent = "{label_text}"')

        for i in range(TOTAL_FRAMES):
            page.screenshot(path=os.path.join(frames_dir, f"frame_{i:04d}.png"), omit_background=True)
            page.wait_for_timeout(1000 / FPS)
            if i % 10 == 0:
                print(f"  frame {i}/{TOTAL_FRAMES}")

        browser.close()

    print(f"Rendered warning '{label_text}' -> {frames_dir}")
    return f"frames_warning_{slug}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render_warning_shake_dynamic.py \"LABEL TEXT\"")
    else:
        render_warning(sys.argv[1])