import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
SAMPLES_DIR = os.path.join(PROJECT_ROOT, "samples")
RENDERER_DIR = os.path.join(PROJECT_ROOT, "renderer")


def build_and_run(scene_json_path):
    with open(scene_json_path, "r") as f:
        spec = json.load(f)

    source_video = os.path.join(SAMPLES_DIR, spec["source_video"])
    logo_path = os.path.join(SAMPLES_DIR, spec["logo"])
    output_path = os.path.join(SAMPLES_DIR, spec["output_name"])
    scenes = spec["scenes"]

    cmd = ["ffmpeg", "-y", "-i", source_video]

    for scene in scenes:
        frames_path = os.path.join(RENDERER_DIR, scene["frames_folder"], "frame_%04d.png")
        cmd += ["-itsoffset", str(scene["start_time"]), "-framerate", "30", "-i", frames_path]

    logo_input_index = len(scenes) + 1
    cmd += ["-i", logo_path]

    filters = []
    filters.append("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg0]")

    for i, scene in enumerate(scenes):
        input_index = i + 1
        start = scene["start_time"]
        end = scene["start_time"] + scene["duration"]
        filters.append(f"[{input_index}:v]format=rgba[fg{input_index}]")
        filters.append(
            f"[bg{i}][fg{input_index}]overlay=0:0:enable='between(t,{start},{end})'[bg{input_index}]"
        )

    last_bg = f"bg{len(scenes)}"
    filters.append(f"[{logo_input_index}:v]scale=160:-1[logo]")
    filters.append(f"[{last_bg}][logo]overlay=40:40[out]")

    filter_complex = ";".join(filters)

    cmd += [
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-map", "0:a:0",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        # No -t limit here anymore - output now runs the full length of the
        # source video automatically, whatever that length is.
        output_path,
    ]

    print("Running ffmpeg with", len(scenes), "scene(s)...")
    subprocess.run(cmd, check=True)
    print(f"Done. Output saved to: {output_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python compose_from_scene.py <scene_file.json>")
    else:
        scene_file = os.path.join(HERE, sys.argv[1])
        build_and_run(scene_file)