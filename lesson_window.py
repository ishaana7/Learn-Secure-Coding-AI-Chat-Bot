import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QFrame
from PySide6.QtCore import Qt, QEvent
from ai_client import get_response, set_api_key

# API key is set in dashboard.py, but included here for safety
# Use the same placeholder or actual key as in dashboard.py
set_api_key("placeholder_key")  # Replace if needed, should match dashboard.py

class LessonWindow(QWidget):
    def __init__(self, title: str = "Lesson"):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(640, 480)
        self.setStyleSheet("background-color: #e6e6e6;")
        self.init_ui(title)

    def init_ui(self, title: str):
        primary_text_color = "#0b3d91"
        main_layout = QVBoxLayout()

        # Heading
        heading = QLabel(title)
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet(f"font-size: 20px; font-weight: bold; margin: 8px; color: {primary_text_color};")
        main_layout.addWidget(heading)

        # Main content: Split layout for AI chatbox and notes
        content_layout = QHBoxLayout()

        # --- Left side: AI Chatbox ---
        chat_frame = QFrame()
        chat_layout = QVBoxLayout()
        chat_frame.setLayout(chat_layout)
        chat_frame.setStyleSheet(f"background-color: {primary_text_color}; border-radius: 10px; padding: 8px;")

        # Chatbox heading
        chat_title = QLabel("AI Chatbox")
        chat_title.setAlignment(Qt.AlignCenter)
        chat_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold; margin: 6px;")
        chat_layout.addWidget(chat_title)
        chat_layout.addStretch()

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet(
            "background-color: white; color: #0b3d91; border-radius: 8px; padding: 8px; font-size: 14px;"
        )
        self.chat_display.setFixedHeight(300)
        chat_layout.addWidget(self.chat_display, alignment=Qt.AlignBottom)

        # Input box (QTextEdit to match DashboardWindow)
        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Type your question here...")
        self.input_box.setFixedHeight(60)
        self.input_box.setStyleSheet(
            "background-color: white; color: #0b3d91; border-radius: 8px; padding: 8px; font-size: 14px;"
        )
        self.input_box.installEventFilter(self)
        chat_layout.addWidget(self.input_box, alignment=Qt.AlignBottom)

        content_layout.addWidget(chat_frame, stretch=1)

        # --- Right side: Notes Section ---
        notes_frame = QFrame()
        notes_layout = QVBoxLayout()
        notes_frame.setLayout(notes_layout)
        notes_frame.setStyleSheet("background-color: #e6e6e6; border-radius: 10px; padding: 8px;")

        # Notes heading
        notes_title = QLabel("Notes")
        notes_title.setAlignment(Qt.AlignCenter)
        notes_title.setStyleSheet(f"font-size: 16px; font-weight: bold; margin: 6px; color: {primary_text_color};")
        notes_layout.addWidget(notes_title)

        # Notes text area
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Type your notes here...")
        self.notes_edit.setStyleSheet(
            "background-color: white; color: #0b3d91; border-radius: 8px; padding: 8px; font-size: 14px;"
        )
        notes_layout.addWidget(self.notes_edit)

        content_layout.addWidget(notes_frame, stretch=1)

        main_layout.addLayout(content_layout)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        close_btn.clicked.connect(self.close)
        main_layout.addWidget(close_btn, alignment=Qt.AlignRight)

        self.setLayout(main_layout)

    # --- Event filter for Enter / Shift+Enter ---
    def eventFilter(self, obj, event):
        if obj == self.input_box and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if event.modifiers() == Qt.ShiftModifier:
                    return False  # Allow newline
                else:
                    self.send_ai_message()
                    return True
        return super().eventFilter(obj, event)

    def send_ai_message(self):
        user_text = self.input_box.toPlainText().strip()
        if not user_text:
            return

        self.chat_display.append(f"<b>You:</b> {user_text}")
        self.input_box.clear()
        self.chat_display.append("<i>AI is thinking...</i>")
        self.chat_display.repaint()  # Force UI update

        try:
            ai_reply = get_response(user_text)
            self.chat_display.append(f"<b>AI:</b> {ai_reply}\n")
        except Exception as e:
            self.chat_display.append(f"<b>Error:</b> {str(e)}\n")
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )

if __name__ == "__main__":
    app = __import__('sys').modules['PySide6.QtWidgets'].QApplication(sys.argv)
    w = LessonWindow("Test Lesson")
    w.show()
    sys.exit(app.exec())