import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
import numpy as np
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
SAMPLES_DIR = os.path.join(PROJECT_ROOT, "samples")
MODEL_PATH = os.path.join(HERE, "selfie_segmenter.tflite")

input_path = os.path.join(SAMPLES_DIR, "new_llc.mp4")

cap = cv2.VideoCapture(input_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, 100)  # jump to frame 100 directly, no need to process earlier frames
success, frame = cap.read()
cap.release()

if not success:
    print("Could not read frame 100")
else:
    cv2.imwrite(os.path.join(HERE, "debug_original_frame.png"), frame)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.ImageSegmenterOptions(base_options=base_options, output_category_mask=True)

    with vision.ImageSegmenter.create_from_options(options) as segmenter:
        result = segmenter.segment(mp_image)
        category_mask = result.category_mask.numpy_view()

        print("Mask shape:", category_mask.shape)
        print("Mask dtype:", category_mask.dtype)
        print("Mask min value:", category_mask.min())
        print("Mask max value:", category_mask.max())
        print("Unique values in mask:", np.unique(category_mask))

        # Save the raw mask itself as a viewable grayscale image
        mask_2d = np.squeeze(category_mask)
        # Scale whatever range it's in up to 0-255 for visibility
        mask_normalized = ((mask_2d - mask_2d.min()) / (mask_2d.max() - mask_2d.min() + 1e-6) * 255).astype(np.uint8)
        cv2.imwrite(os.path.join(HERE, "debug_mask.png"), mask_normalized)

    print("Saved debug_original_frame.png and debug_mask.png to compositor folder")