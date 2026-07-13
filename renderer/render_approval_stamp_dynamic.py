from playwright.sync_api import sync_playwright
import os
import sys
import re

here = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(here, "templates", "approval_stamp.html")

FPS = 30
DURATION = 2.2
TOTAL_FRAMES = int(FPS * DURATION)


def slugify(text, max_len=30):
    slug = re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')
    return slug[:max_len]


def render_stamp(stamp_text, style="approved"):
    # style: "approved" (green) or "declined" (red)
    slug = slugify(stamp_text)
    frames_dir = os.path.join(here, f"frames_stamp_{slug}")
    os.makedirs(frames_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(f"file:///{html_path.replace(os.sep, '/')}")

        page.evaluate(f'document.getElementById("stampText").textContent = "{stamp_text}"')
        if style == "declined":
            page.evaluate('document.getElementById("stamp").classList.add("declined")')

        for i in range(TOTAL_FRAMES):
            page.screenshot(path=os.path.join(frames_dir, f"frame_{i:04d}.png"), omit_background=True)
            page.wait_for_timeout(1000 / FPS)
            if i % 10 == 0:
                print(f"  frame {i}/{TOTAL_FRAMES}")

        browser.close()

    print(f"Rendered stamp '{stamp_text}' ({style}) -> {frames_dir}")
    return f"frames_stamp_{slug}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render_approval_stamp_dynamic.py \"TEXT\" [approved|declined]")
    else:
        text = sys.argv[1]
        style = sys.argv[2] if len(sys.argv) > 2 else "approved"
        render_stamp(text, style)