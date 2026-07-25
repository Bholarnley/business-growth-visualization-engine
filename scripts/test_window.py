from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
import sys

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("BGVE - Test Window")
window.resize(400, 200)

layout = QVBoxLayout()
label = QLabel("BGVE Desktop App - Phase 7 Starting")
layout.addWidget(label)
window.setLayout(layout)

window.show()
sys.exit(app.exec())