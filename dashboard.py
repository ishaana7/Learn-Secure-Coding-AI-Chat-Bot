# dashboard.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTextEdit, QApplication
)
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
from PySide6.QtCore import Qt, QEvent

from ai_client import get_response, set_api_key
from lesson_window import LessonWindow  # <-- Import your LessonWindow

# Set API key once
set_api_key("your_api_key_here")


class ProgressCircle(QWidget):
    def __init__(self, progress=0.0):
        super().__init__()
        self.progress = progress
        self.setFixedSize(60, 60)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center = self.rect().center()
        radius = 25

        # Background circle (gray)
        painter.setPen(QPen(QColor(200, 200, 200), 3))
        painter.setBrush(QBrush(Qt.transparent))
        painter.drawEllipse(center.x() - radius, center.y() - radius, radius * 2, radius * 2)

        # Progress circle (green)
        if self.progress > 0:
            painter.setPen(QPen(QColor(34, 139, 34), 3))
            start_angle = 90 * 16
            span_angle = -int(360 * self.progress * 16)
            painter.drawArc(center.x() - radius, center.y() - radius, radius * 2, radius * 2, start_angle, span_angle)


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.lessons = [
            {
                "title": "Input Validation",
                "start_prompt": (
                    "You are a security-focused instructor. Teach the student about **input validation** "
                    "in web applications. Explain why it matters, common pitfalls (e.g., SQLi, XSS), "
                    "and give a short Python/Flask example of safe validation using `werkzeug` utilities."
                ),
                "challenge": (
                    "Challenge: Write a Flask route `/login` that safely validates a username (alphanumeric, "
                    "3–20 chars) and a password (at least 8 chars, one uppercase, one digit). "
                    "Return JSON `{'status': 'valid'}` or `{'status': 'invalid', 'errors': [...]}`."
                ),
                "progress": 1.0
            },
            {
                "title": "Auth & Sessions",
                "start_prompt": (
                    "You are a security instructor. Explain **authentication** and **session management**. "
                    "Cover password hashing (bcrypt/argon2), secure cookies, session fixation, "
                    "and how Flask-Login or Django’s auth system helps."
                ),
                "challenge": (
                    "Challenge: Implement a secure login endpoint in Flask that hashes the password with bcrypt, "
                    "stores the user ID in a HttpOnly, Secure, SameSite=Strict session cookie, "
                    "and returns a JSON Web Token (JWT) for subsequent API calls."
                ),
                "progress": 0.5
            },
            {
                "title": "Access Control",
                "start_prompt": (
                    "You are a security teacher. Walk the student through **access control** (RBAC/ABAC). "
                    "Show why checking permissions on every request matters, "
                    "and demonstrate a simple decorator in Flask that enforces role-based checks."
                ),
                "challenge": (
                    "Challenge: Create a `@require_role('admin')` decorator. "
                    "Apply it to a `/users` endpoint that lists all users only for admins. "
                    "Non-admins should receive `403 Forbidden`."
                ),
                "progress": 0.25
            },
            {
                "title": "Error Handling",
                "start_prompt": (
                    "You are a security instructor. Teach **secure error handling**. "
                    "Explain why stack traces must never leak to users, how to log errors safely, "
                    "and how to return generic but helpful messages."
                ),
                "challenge": (
                    "Challenge: In a Flask app, register a global error handler for `500` errors. "
                    "Log the exception with `logging.exception`, return JSON `{'error': 'Internal Server Error'}`, "
                    "and ensure the response never contains traceback data."
                ),
                "progress": 0.0
            },
        ]
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Secure Learning Chatbox - Dashboard")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: #e6e6e6;")

        primary_text_color = "#0b3d91"
        main_layout = QHBoxLayout()

        # --- Left side (Progress + Continue Learning) ---
        left_layout = QVBoxLayout()
        left_widget = QFrame()
        left_widget.setLayout(left_layout)
        left_widget.setStyleSheet("background-color: #e6e6e6; border-radius: 10px; padding: 12px;")

        # Progress Section
        progress_layout = QVBoxLayout()
        progress_title = QLabel("Learning Progress")
        progress_title.setAlignment(Qt.AlignCenter)
        progress_title.setStyleSheet(
            f"font-size: 18px; font-weight: bold; margin: 20px; color: {primary_text_color};"
        )
        progress_layout.addWidget(progress_title)

        # Progress circles
        circles_layout = QHBoxLayout()
        circles_layout.setAlignment(Qt.AlignCenter)
        for prog in [1.0, 0.5, 0.25, 0.0]:
            circles_layout.addWidget(ProgressCircle(prog))
        progress_layout.addLayout(circles_layout)

        # Labels under circles
        labels_layout = QHBoxLayout()
        labels_layout.setAlignment(Qt.AlignCenter)
        labels = ["Complete", "In Progress", "Started", "Not Started"]
        for text in labels:
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(f"font-size: 10px; margin: 5px; color: {primary_text_color};")
            labels_layout.addWidget(label)
        progress_layout.addLayout(labels_layout)

        # Continue Learning button
        continue_btn = QPushButton("Continue Learning")
        continue_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                margin: 30px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        continue_btn.clicked.connect(self.continue_learning)

        # Center container for button + lesson buttons
        center_container = QFrame()
        center_layout = QVBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(12)
        center_layout.setAlignment(Qt.AlignHCenter)
        center_container.setLayout(center_layout)
        center_layout.addWidget(continue_btn, alignment=Qt.AlignHCenter)

        # --- LESSON BUTTONS (clickable) ---
        lessons_layout = QHBoxLayout()
        lessons_layout.setSpacing(24)
        lessons_layout.setContentsMargins(0, 12, 0, 12)
        semi_border = "rgba(11,61,145,0.55)"

        for idx, lesson in enumerate(self.lessons):
            btn = QPushButton(lesson["title"].split()[0])
            btn.setFixedSize(90, 50)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: 2px solid {semi_border};
                    border-radius: 8px;
                    color: {primary_text_color};
                    font-weight: 600;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background-color: rgba(11,61,145,0.08);
                }}
            """)
            btn.clicked.connect(lambda checked, i=idx: self.open_lesson_window(i))

            name_label = QLabel(lesson["title"])
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet(f"font-size: 10px; margin: 5px; color: {primary_text_color};")

            col = QVBoxLayout()
            col.setAlignment(Qt.AlignCenter)
            col.setSpacing(5)
            col.addWidget(btn)
            col.addWidget(name_label)
            lessons_layout.addLayout(col)

        lessons_frame = QFrame()
        lessons_frame.setLayout(lessons_layout)
        lessons_frame.setStyleSheet("background: transparent;")
        center_layout.addWidget(lessons_frame, alignment=Qt.AlignCenter)

        left_layout.addLayout(progress_layout)
        left_layout.addWidget(center_container, alignment=Qt.AlignHCenter)
        left_layout.addStretch()

        # --- Right side (AI Chatbox) ---
        right_layout = QVBoxLayout()
        right_widget = QFrame()
        right_widget.setLayout(right_layout)
        right_widget.setStyleSheet(f"background-color: {primary_text_color}; border-radius: 10px; padding: 8px;")
        right_widget.setFixedWidth(240)

        right_title = QLabel("AI Chatbox")
        right_title.setAlignment(Qt.AlignCenter)
        right_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold; margin: 6px;")
        right_layout.addWidget(right_title)
        right_layout.addStretch()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet(
            "background-color: white; color: #0b3d91; border-radius: 8px; padding: 8px;"
        )
        self.chat_display.setFixedHeight(400)
        right_layout.addWidget(self.chat_display, alignment=Qt.AlignBottom)

        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Type your question here...")
        self.notes_edit.setFixedHeight(60)
        self.notes_edit.setStyleSheet(
            "background-color: white; color: #0b3d91; border-radius: 8px; padding: 8px;"
        )
        self.notes_edit.installEventFilter(self)
        right_layout.addWidget(self.notes_edit, alignment=Qt.AlignBottom)

        main_layout.addWidget(left_widget, stretch=3)
        main_layout.addWidget(right_widget, stretch=1)
        self.setLayout(main_layout)

    # --- Event filter for Enter / Shift+Enter ---
    def eventFilter(self, obj, event):
        if obj == self.notes_edit and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if event.modifiers() == Qt.ShiftModifier:
                    return False
                else:
                    self.send_ai_message()
                    return True
        return super().eventFilter(obj, event)

    # --- Send AI message (dashboard chat) ---
    def send_ai_message(self):
        user_text = self.notes_edit.toPlainText().strip()
        if not user_text:
            return

        self.chat_display.append(f"<b>You:</b> {user_text}")
        self.notes_edit.clear()
        self.chat_display.append("<i>AI is thinking...</i>")
        QApplication.processEvents()

        try:
            ai_reply = get_response(user_text)
            self.chat_display.append(f"<b>AI:</b> {ai_reply}\n")
        except Exception as e:
            self.chat_display.append(f"<b>Error:</b> {e}\n")
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )

    # --- NEW: Open LessonWindow and auto-start lesson ---
    def open_lesson_window(self, lesson_idx: int):
        lesson = self.lessons[lesson_idx]

        # Create and show the lesson window
        lesson_win = LessonWindow(lesson["title"])
        lesson_win.show()

        # Auto-send teaching prompt
        lesson_win.chat_display.append(f"<b>System:</b> {lesson['start_prompt']}")
        lesson_win.chat_display.append("<i>AI is thinking...</i>")
        QApplication.processEvents()

        try:
            reply = get_response(lesson["start_prompt"])
            lesson_win.chat_display.append(f"<b>AI:</b> {reply}\n")
        except Exception as e:
            lesson_win.chat_display.append(f"<b>Error:</b> {e}\n")

        # Auto-send challenge
        lesson_win.chat_display.append(f"<b>Challenge:</b> {lesson['challenge']}")
        lesson_win.chat_display.append("<i>AI waiting for your solution…</i>")

    # --- Continue Learning button ---
    def continue_learning(self):
        for idx, lesson in enumerate(self.lessons):
            if lesson["progress"] < 1.0:
                self.open_lesson_window(idx)
                return
        self.open_lesson_window(0)  # fallback