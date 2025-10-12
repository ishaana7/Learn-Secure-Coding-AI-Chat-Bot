import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import Qt


class LessonWindow(QWidget):
    def __init__(self, title: str = "Lesson"):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(640, 480)
        # Match dashboard background
        self.setStyleSheet("background-color: #e6e6e6;")
        self.init_ui(title)

    def init_ui(self, title: str):
        layout = QVBoxLayout()

        heading = QLabel(title)
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet("font-size: 20px; font-weight: bold; margin: 8px;")
        layout.addWidget(heading)

        body = QTextEdit()
        body.setReadOnly(False)
        body.setPlaceholderText("Lesson contents go here. You can type notes or experiment.")
        layout.addWidget(body)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

        self.setLayout(layout)


if __name__ == "__main__":
    # quick manual test runner
    app = __import__('sys').modules['PySide6.QtWidgets'].QApplication(sys.argv)
    w = LessonWindow("Test Lesson")
    w.show()
    sys.exit(app.exec())
