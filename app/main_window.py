from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QTextEdit, QFileDialog, QLineEdit, QProgressBar
)
from PySide6.QtCore import QThread, Signal
import sys
import os
import json
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
SAMPLES_DIR = os.path.join(PROJECT_ROOT, "samples")
SCENE_GEN_DIR = os.path.join(PROJECT_ROOT, "scene_generator")
sys.path.insert(0, SCENE_GEN_DIR)

from script_to_scene_lite import estimate_scenes


class RenderWorker(QThread):
    finished_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, scene_json_path):
        super().__init__()
        self.scene_json_path = scene_json_path

    def run(self):
        try:
            compose_script = os.path.join(SCENE_GEN_DIR, "compose_from_scene.py")
            result = subprocess.run(
                ["python", compose_script, os.path.basename(self.scene_json_path)],
                cwd=SCENE_GEN_DIR,
                capture_output=True, text=True
            )
            if result.returncode == 0:
                self.finished_signal.emit(result.stdout)
            else:
                self.error_signal.emit(result.stderr)
        except Exception as e:
            self.error_signal.emit(str(e))


class BGVEMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BGVE - Business Growth Visualization Engine")
        self.resize(600, 620)

        self.video_path = None
        self.video_filename = None
        self.generated_scenes = None

        layout = QVBoxLayout()

        layout.addWidget(QLabel("1. Select your recorded video:"))
        self.video_label = QLineEdit()
        self.video_label.setReadOnly(True)
        self.video_label.setPlaceholderText("No video selected yet")
        layout.addWidget(self.video_label)

        select_video_btn = QPushButton("Choose Video File...")
        select_video_btn.clicked.connect(self.choose_video)
        layout.addWidget(select_video_btn)

        layout.addWidget(QLabel("2. Paste your script:"))
        self.script_box = QTextEdit()
        self.script_box.setPlaceholderText("Paste your video script here...")
        layout.addWidget(self.script_box)

        generate_btn = QPushButton("Generate Scenes")
        generate_btn.clicked.connect(self.generate_scenes)
        layout.addWidget(generate_btn)

        layout.addWidget(QLabel("3. Scene preview:"))
        self.preview_box = QTextEdit()
        self.preview_box.setReadOnly(True)
        layout.addWidget(self.preview_box)

        export_btn = QPushButton("Render & Export Video")
        export_btn.clicked.connect(self.export_video)
        layout.addWidget(export_btn)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # indeterminate spinner style
        self.progress.hide()
        layout.addWidget(self.progress)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def choose_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select your video", "", "Video Files (*.mp4 *.mov)"
        )
        if file_path:
            self.video_path = file_path
            self.video_filename = os.path.basename(file_path)
            self.video_label.setText(self.video_filename)

    def generate_scenes(self):
        script_text = self.script_box.toPlainText().strip()
        if not script_text:
            self.status_label.setText("Please paste a script first.")
            return
        try:
            result = estimate_scenes(script_text)
            self.generated_scenes = result
            pretty_json = json.dumps(result, indent=2, ensure_ascii=False)
            self.preview_box.setPlainText(pretty_json)
            self.status_label.setText(f"Generated {len(result['scenes'])} scene(s). Review above.")
        except Exception as e:
            self.status_label.setText(f"Error generating scenes: {e}")

    def export_video(self):
        if not self.video_filename:
            self.status_label.setText("Please select a video first.")
            return
        if not self.generated_scenes:
            self.status_label.setText("Please generate scenes first.")
            return

        # Build the full scene spec (video/logo/output) and save it
        full_spec = {
            "source_video": self.video_filename,
            "logo": "logo_MJB.jpg",
            "output_name": "app_export_output.mp4",
            "scenes": self.generated_scenes["scenes"],
        }
        scene_json_path = os.path.join(SCENE_GEN_DIR, "app_generated_scene.json")
        with open(scene_json_path, "w", encoding="utf-8") as f:
            json.dump(full_spec, f, indent=2, ensure_ascii=False)

        self.status_label.setText("Rendering... this may take a while.")
        self.progress.show()

        self.worker = RenderWorker(scene_json_path)
        self.worker.finished_signal.connect(self.on_render_done)
        self.worker.error_signal.connect(self.on_render_error)
        self.worker.start()

    def on_render_done(self, output):
        self.progress.hide()
        self.status_label.setText("Done! Check samples/app_export_output.mp4")

    def on_render_error(self, error):
        self.progress.hide()
        self.status_label.setText(f"Render failed: {error[:200]}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BGVEMainWindow()
    window.show()
    sys.exit(app.exec())