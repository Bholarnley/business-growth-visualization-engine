from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QTextEdit, QFileDialog, QLineEdit
)
import sys
import os

class BGVEMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BGVE - Business Growth Visualization Engine")
        self.resize(600, 500)

        self.video_path = None

        layout = QVBoxLayout()

        # Video selection
        layout.addWidget(QLabel("1. Select your recorded video:"))
        self.video_label = QLineEdit()
        self.video_label.setReadOnly(True)
        self.video_label.setPlaceholderText("No video selected yet")
        layout.addWidget(self.video_label)

        select_video_btn = QPushButton("Choose Video File...")
        select_video_btn.clicked.connect(self.choose_video)
        layout.addWidget(select_video_btn)

        # Script input
        layout.addWidget(QLabel("2. Paste your script:"))
        self.script_box = QTextEdit()
        self.script_box.setPlaceholderText("Paste your video script here...")
        layout.addWidget(self.script_box)

        # Generate button (not wired yet - Stage 2)
        generate_btn = QPushButton("Generate Scenes")
        generate_btn.clicked.connect(self.generate_scenes)
        layout.addWidget(generate_btn)

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
        # Placeholder for now - Stage 2 wires this to the real scene generator
        self.status_label.setText("Generate Scenes clicked - not wired up yet")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BGVEMainWindow()
    window.show()
    sys.exit(app.exec())