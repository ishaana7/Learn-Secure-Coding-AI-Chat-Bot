import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QFrame, QApplication
)
from PySide6.QtCore import Qt, QEvent
from ai_client import get_response, set_api_key

# Match dashboard key behavior
set_api_key("placeholder_key")


class LessonWindow(QWidget):
    def __init__(self, title: str = "Lesson"):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(640, 640)
        self.setStyleSheet("background-color: #e6e6e6;")
        self.init_ui(title)

    def init_ui(self, title: str):
        primary_text_color = "#0b3d91"
        main_layout = QVBoxLayout()

        # Heading
        heading = QLabel(title)
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet(
            f"font-size: 20px; font-weight: bold; margin: 8px; color: {primary_text_color};"
        )
        main_layout.addWidget(heading)

        # Main content area (AI chat left, Notes right)
        content_layout = QHBoxLayout()

        # =========================================================
        # ===============  LEFT SIDE: CHAT AREA ===================
        # =========================================================
        chat_frame = QFrame()
        chat_frame.setStyleSheet(
            f"background-color: {primary_text_color}; border-radius: 10px; padding: 8px;"
        )
        chat_outer_layout = QVBoxLayout(chat_frame)

        # Chat title
        chat_title = QLabel("AI Chatbox")
        chat_title.setAlignment(Qt.AlignCenter)
        chat_title.setStyleSheet(
            "color: white; font-size: 16px; font-weight: bold; margin: 6px;"
        )
        chat_outer_layout.addWidget(chat_title)

        # -------- AI RESPONSE BOX (top frame) --------
        response_frame = QFrame()
        response_layout = QVBoxLayout(response_frame)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet(
            "background-color: white; color: #0b3d91; border-radius: 8px; "
            "padding: 8px; font-size: 14px;"
        )
        response_layout.addWidget(self.chat_display)

        chat_outer_layout.addWidget(response_frame, stretch=3)

        # -------- USER INPUT BOX (bottom frame) --------
        input_frame = QFrame()
        input_layout = QVBoxLayout(input_frame)

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Type your question here...")
        self.input_box.setFixedHeight(70)
        self.input_box.setStyleSheet(
            "background-color: white; color: #0b3d91; border-radius: 8px; "
            "padding: 8px; font-size: 14px;"
        )
        self.input_box.installEventFilter(self)

        input_layout.addWidget(self.input_box)
        chat_outer_layout.addWidget(input_frame, stretch=1)

        content_layout.addWidget(chat_frame, stretch=1)

        # =========================================================
        # ===============  RIGHT SIDE: NOTES ======================
        # =========================================================
        notes_frame = QFrame()
        notes_frame.setStyleSheet(
            "background-color: #e6e6e6; border-radius: 10px; padding: 8px;"
        )
        notes_layout = QVBoxLayout(notes_frame)

        notes_title = QLabel("Notes")
        notes_title.setAlignment(Qt.AlignCenter)
        notes_title.setStyleSheet(
            f"font-size: 16px; font-weight: bold; margin: 6px; color: {primary_text_color};"
        )
        notes_layout.addWidget(notes_title)

        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Type your notes here...")
        self.notes_edit.setStyleSheet(
            "background-color: white; color: #0b3d91; border-radius: 8px; "
            "padding: 8px; font-size: 14px;"
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

    # ENTER key behavior
    def eventFilter(self, obj, event):
        if obj == self.input_box and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if event.modifiers() == Qt.ShiftModifier:
                    return False  # new line allowed
                else:
                    self.send_ai_message()
                    return True
        return super().eventFilter(obj, event)

    # Sending message to AI
    def send_ai_message(self):
        user_text = self.input_box.toPlainText().strip()
        if not user_text:
            return

        self.chat_display.append(f"<b>You:</b> {user_text}")
        self.input_box.clear()
        self.chat_display.append("<i>AI is thinking...</i>")
        self.chat_display.repaint()

        try:
            ai_reply = get_response(user_text)
            self.chat_display.append(f"<b>AI:</b> {ai_reply}\n")
        except Exception as e:
            self.chat_display.append(f"<b>Error:</b> {str(e)}\n")

        # Auto-scroll
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = LessonWindow("Test Lesson")
    w.show()
    sys.exit(app.exec())
