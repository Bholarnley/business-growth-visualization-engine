import json
import os
import subprocess
import sys
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
RENDERER_DIR = os.path.join(PROJECT_ROOT, "renderer")


def slugify(text, max_len=40):
    slug = re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')
    return slug[:max_len]


def extract_caption_text(reason):
    # The "reason" field looks like: General narrative sentence (fallback caption): "actual text"
    # This pulls out just the quoted sentence.
    match = re.search(r'"([^"]+)"', reason)
    return match.group(1) if match else reason


def main(scene_json_path):
    with open(scene_json_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    changed = False
    for scene in spec["scenes"]:
        if scene["template"] == "text_highlight":
            caption_text = extract_caption_text(scene["reason"])
            slug = slugify(caption_text)
            expected_folder = f"frames_text_highlight_{slug}"
            folder_path = os.path.join(RENDERER_DIR, expected_folder)

            if not os.path.isdir(folder_path):
                print(f"Rendering caption: {caption_text[:60]}...")
                render_script = os.path.join(RENDERER_DIR, "render_text_highlight_dynamic.py")
                subprocess.run(["python", render_script, caption_text], check=True)
            else:
                print(f"Already rendered, skipping: {caption_text[:60]}...")

            scene["frames_folder"] = expected_folder
            changed = True

    if changed:
        with open(scene_json_path, "w", encoding="utf-8") as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)
        print(f"\nUpdated {scene_json_path} with correct per-caption frame folders.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render_all_captions.py <scene_file.json>")
    else:
        scene_file = os.path.join(HERE, sys.argv[1])
        main(scene_file)