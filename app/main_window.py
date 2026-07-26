from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QTextEdit, QFileDialog, QLineEdit
)
import sys
import os
import json

# Let this file find scene_generator's code, regardless of where the app is launched from
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scene_generator"))

from script_to_scene_lite import estimate_scenes


class BGVEMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BGVE - Business Growth Visualization Engine")
        self.resize(600, 550)

        self.video_path = None
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

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def choose_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select your video", "", "Video Files (*.mp4 *.mov)"
        )
        if file_path:
            self.video_path = file_path
            self.video_label.setText(os.path.basename(file_path))

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
            scene_count = len(result["scenes"])
            self.status_label.setText(f"Generated {scene_count} scene(s). Review above.")
        except Exception as e:
            self.status_label.setText(f"Error generating scenes: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BGVEMainWindow()
    window.show()
    sys.exit(app.exec())