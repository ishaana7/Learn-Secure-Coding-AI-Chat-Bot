import threading
from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTextEdit, QApplication, QScrollBar # Added QScrollBar for explicit type
)
from PySide6.QtGui import QMovie, QPainter, QPen, QBrush, QColor, QTextCursor 
from PySide6.QtCore import Qt, QEvent, QTimer, QThreadPool # QThreadPool is no longer used for AIWorker, but kept for context

# Assuming ai_client is imported implicitly or not needed here
from ai_worker import AIWorker 

class ProgressCircle(QWidget):
    def __init__(self, progress: float = 0.0):
        super().__init__()
        self.progress = progress
        self.setFixedSize(60, 60)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center = self.rect().center()
        radius = 25

        # Gray outer circle
        painter.setPen(QPen(QColor(200, 200, 200), 3))
        painter.setBrush(QBrush(Qt.transparent))
        painter.drawEllipse(center.x()-radius, center.y()-radius, radius*2, radius*2)

        # Green progress arc
        if self.progress > 0:
            painter.setPen(QPen(QColor(34, 139, 34), 3))
            start_angle = 90 * 16
            span_angle = -int(360 * self.progress * 16)
            painter.drawArc(center.x()-radius, center.y()-radius,
                            radius*2, radius*2, start_angle, span_angle)


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.lessons = [
            {
                "title": "Input Validation",
                "start_prompt": (
                    "Give a short intro to input validation: what it is, why it matters, "
                    "and a tiny Flask example."
                ),
                "challenge": (
                    "Flask /login route: username alnum 3-20 chars, password min 8 chars "
                    "w/ uppercase+digit. Return JSON status."
                ),
                "progress": 1.0
            },
            {
                "title": "Auth & Sessions",
                "start_prompt": (
                    "Briefly explain authentication and session management: "
                    "hashing (bcrypt), secure cookies, session fixation."
                ),
                "challenge": (
                    "Implement secure Flask login: bcrypt hash, secure HttpOnly SameSite "
                    "cookie, return JWT."
                ),
                "progress": 0.5
            },
            {
                "title": "Access Control",
                "start_prompt": (
                    "Explain RBAC vs ABAC and why permission checks must happen on every request."
                ),
                "challenge": (
                    "Write a Flask decorator @require_role('admin') and protect /users "
                    "endpoint; others get 403."
                ),
                "progress": 0.25
            },
            {
                "title": "Error Handling",
                "start_prompt": (
                    "Explain secure error handling: don't expose stack traces, log safely, "
                    "return a generic message."
                ),
                "challenge": (
                    "Add global Flask 500 handler which logs exception and returns a safe "
                    "JSON message."
                ),
                "progress": 0.0
            }
        ]
        
        # QThreadPool is no longer used for AI calls, but kept if needed later
        self.threadpool = QThreadPool() 
        
        # New attribute to prevent the AIWorker from being garbage collected
        self._current_worker = None
        
        # 🎯 FIX: The method call that was causing the AttributeError
        self.init_ui() 

    # 🎯 FIX: The method definition was missing or misplaced
    def init_ui(self):
        self.setWindowTitle("Secure Learning Chatbox - Dashboard")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: #e6e6e6;")
        primary_text_color = "#0b3d91"

        main_layout = QHBoxLayout()

        # -------------------- LEFT PANEL --------------------
        left_layout = QVBoxLayout()
        left_widget = QFrame()
        left_widget.setLayout(left_layout)
        left_widget.setStyleSheet("background-color: #e6e6e6; border-radius: 10px; padding: 12px;")

        # Progress section
        prog_layout = QVBoxLayout()
        title = QLabel("Learning Progress")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; margin: 20px; color:{primary_text_color};")
        prog_layout.addWidget(title)

        circles = QHBoxLayout()
        circles.setAlignment(Qt.AlignCenter)
        for lesson in self.lessons:
            circles.addWidget(ProgressCircle(lesson["progress"]))
        prog_layout.addLayout(circles)
        left_layout.addLayout(prog_layout)

        # Continue button
        continue_btn = QPushButton("Continue Learning")
        continue_btn.setStyleSheet("""
            QPushButton { background-color:#4CAF50; color:white; border:none;
                          padding:15px 30px; font-size:16px; font-weight:bold;
                          border-radius:8px; margin:12px; }
            QPushButton:hover { background-color:#45a049; }
        """)
        continue_btn.clicked.connect(self.continue_learning)
        left_layout.addWidget(continue_btn, alignment=Qt.AlignHCenter)

        # Lesson selector buttons
        lessons_layout = QHBoxLayout()
        lessons_layout.setSpacing(10) 
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

            v = QVBoxLayout()
            v.setAlignment(Qt.AlignHCenter | Qt.AlignTop) 
            
            v.addWidget(btn, alignment=Qt.AlignHCenter)

            lbl = QLabel(lesson["title"])
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"font-size:10px; color:{primary_text_color}; margin:1px 5px;")
            v.addWidget(lbl)

            lessons_layout.addLayout(v)

        lessons_frame = QFrame()
        lessons_frame.setLayout(lessons_layout)
        left_layout.addWidget(lessons_frame)
        left_layout.addStretch()

        # -------------------- RIGHT PANEL --------------------
        right_layout = QVBoxLayout()
        right_widget = QFrame()
        right_widget.setLayout(right_layout)
        right_widget.setStyleSheet(f"background-color:{primary_text_color}; border-radius:10px; padding:8px;")
        right_widget.setFixedWidth(320)

        rtitle = QLabel("AI Chatbox")
        rtitle.setAlignment(Qt.AlignCenter)
        rtitle.setStyleSheet("color:white; font-size:16px; font-weight:bold; margin:6px;")
        right_layout.addWidget(rtitle)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFixedHeight(360)
        self.chat_display.setStyleSheet("background:white; color:#0b3d91; border-radius:8px; padding:8px;")
        right_layout.addWidget(self.chat_display)

        # Spinner for the Dashboard Quick Chat
        self.spinner = QLabel()
        self.spinner.setAlignment(Qt.AlignCenter)
        try:
            # Assumes 'spinner.gif' is available in the same directory
            movie = QMovie("spinner.gif")
            if movie.isValid():
                self.spinner.setMovie(movie)
                movie.start()
            else:
                raise Exception()
        except Exception:
            self.spinner.setText("<b style='color:white'>AI is generating...</b>")
            
        self.spinner.hide()
        right_layout.addWidget(self.spinner)

        self.quick_input = QTextEdit()
        self.quick_input.setFixedHeight(60)
        self.quick_input.setPlaceholderText("Ask a quick question…")
        self.quick_input.setStyleSheet("background:white; color:#0b3d91; border-radius:8px; padding:8px;")
        self.quick_input.installEventFilter(self)
        right_layout.addWidget(self.quick_input)

        main_layout.addWidget(left_widget, stretch=3)
        main_layout.addWidget(right_widget, stretch=1)
        self.setLayout(main_layout)

    # -------------------- EVENT FILTER --------------------
    def eventFilter(self, obj, event):
        if obj == self.quick_input and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter) and not event.modifiers():
                self._on_quick_send()
                return True
        return super().eventFilter(obj, event)

    # -------------------- SEND MESSAGE --------------------
    def _on_quick_send(self):
        text = self.quick_input.toPlainText().strip()
        if not text:
            return

        self.chat_display.append(f"<b>You:</b> {text}\n")
        self.quick_input.clear()
        
        # Show the spinner
        self.spinner.show()
        QApplication.processEvents()

        worker = AIWorker(text)
        worker.signals.finished.connect(self._display_quick_reply)
        worker.signals.error.connect(lambda r: self._display_quick_reply(r))
        
        # Keep a reference to prevent garbage collection while the thread runs
        self._current_worker = worker 
        
        worker.run() # 🎯 RUN THE WORKER IN A NEW THREAD

    # -------------------- FIXED STREAMING --------------------
    def _display_quick_reply(self, reply_text: Optional[str]):
        # Clear the worker reference once done
        if self._current_worker:
            del self._current_worker
            self._current_worker = None
        
        # Hide the spinner
        self.spinner.hide()
        
        self.chat_display.append("<b>AI:</b> ")

        if reply_text is None:
            self.chat_display.append("<i style='color:red'>API Error – check key/network</i>")
            return

        if not reply_text:
            reply_text = "(no response)"

        chunk = 35
        idx = 0

        # Note: We must explicitly cast to QScrollBar if the linter complains
        # about `verticalScrollBar()`, though it usually works fine implicitly.
        vertical_scroll_bar: QScrollBar = self.chat_display.verticalScrollBar()

        def step():
            nonlocal idx
            if idx >= len(reply_text):
                self.chat_display.append("\n")
                return

            end = min(idx + chunk, len(reply_text))
            piece = reply_text[idx:end]

            cur = self.chat_display.textCursor()
            cur.movePosition(QTextCursor.MoveOperation.End) 
            cur.insertText(piece)

            vertical_scroll_bar.setValue(vertical_scroll_bar.maximum())

            idx = end
            QTimer.singleShot(25, step)

        QTimer.singleShot(0, step)

    # -------------------- LESSON WINDOWS --------------------
    def open_lesson_window(self, idx):
        # NOTE: Make sure lesson_window.py is in the same directory and LessonWindow 
        # is correctly implemented using the threading fix.
        from lesson_window import LessonWindow 
        win = LessonWindow(self.lessons[idx])
        win.show()

    def continue_learning(self):
        for idx, lesson in enumerate(self.lessons):
            if lesson["progress"] < 1.0:
                self.open_lesson_window(idx)
                return
        self.open_lesson_window(0)