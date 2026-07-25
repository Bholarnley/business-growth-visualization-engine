import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
import numpy as np
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
SAMPLES_DIR = os.path.join(PROJECT_ROOT, "samples")
RENDERER_DIR = os.path.join(PROJECT_ROOT, "renderer")
MODEL_PATH = os.path.join(HERE, "selfie_segmenter.tflite")


def replace_background(input_video, background_image, output_video, threshold=127):
    input_path = os.path.join(SAMPLES_DIR, input_video)
    bg_path = os.path.join(RENDERER_DIR, background_image)
    output_path = os.path.join(SAMPLES_DIR, output_video)

    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    bg_image = cv2.imread(bg_path)
    bg_image = cv2.resize(bg_image, (width, height))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.ImageSegmenterOptions(
        base_options=base_options,
        output_category_mask=True,
    )

    with vision.ImageSegmenter.create_from_options(options) as segmenter:
        frame_num = 0
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            result = segmenter.segment(mp_image)
            category_mask = result.category_mask.numpy_view()

            mask_2d = np.squeeze(category_mask)
            # CONFIRMED via debug: 0 = person, 255 = background (inverted from
            # the usual assumption) - so "is_person" means LOW values, not high.
            is_person = mask_2d < threshold
            condition = np.repeat(is_person[:, :, np.newaxis], 3, axis=2)

            output_frame = np.where(condition, frame, bg_image)
            out.write(output_frame)

            frame_num += 1
            if frame_num % 30 == 0:
                print(f"  frame {frame_num}/{total_frames}")

    cap.release()
    out.release()
    print(f"Done. Saved to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python replace_background.py <input_video> <background_image> <output_video>")
    else:
        replace_background(sys.argv[1], sys.argv[2], sys.argv[3])