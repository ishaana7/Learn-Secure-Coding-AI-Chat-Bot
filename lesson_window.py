import threading
from typing import Optional
from PySide6.QtWidgets import (
    # 🎯 FIX: Ensure QWidget and other classes are imported
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame, QApplication, QScrollBar
)
from PySide6.QtCore import Qt, QEvent, QTimer, QThreadPool
from PySide6.QtGui import QMovie, QTextCursor 
from ai_worker import AIWorker

class LessonWindow(QWidget):
    def __init__(self, lesson: dict):
        super().__init__()
        self.lesson = lesson
        self.setWindowTitle(self.lesson.get("title", "Lesson"))
        self.setFixedSize(640, 640)
        self.setStyleSheet("background-color: #e6e6e6;")
        
        # QThreadPool is no longer used for AI calls, but kept if needed later
        self.threadpool = QThreadPool()
        self.challenge_printed = False 
        
        # New attribute to hold the worker reference
        self._current_worker = None 
        
        self._build_ui()

    def _build_ui(self):
        primary = "#0b3d91"
        main = QVBoxLayout()

        heading = QLabel(self.lesson.get("title", "Lesson"))
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet(f"font-size: 20px; font-weight: bold; margin: 8px; color: {primary};")
        main.addWidget(heading)

        content = QHBoxLayout()

        # ---------- LEFT: chat ----------
        chat_frame = QFrame()
        chat_frame.setStyleSheet(f"background-color: {primary}; border-radius: 10px; padding: 8px;")
        chat_lay = QVBoxLayout(chat_frame)

        chat_title = QLabel("AI Chatbox")
        chat_title.setAlignment(Qt.AlignCenter)
        chat_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold; margin: 6px;")
        chat_lay.addWidget(chat_title)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: white; color: #0b3d91; border-radius: 8px; padding: 8px; font-size: 14px;")
        chat_lay.addWidget(self.chat_display, stretch=3)

        # Spinner Initialization (Updated for QMovie)
        self.spinner = QLabel()
        self.spinner.setAlignment(Qt.AlignCenter)
        try:
            movie = QMovie("spinner.gif")
            if movie.isValid():
                self.spinner.setMovie(movie)
                movie.start()
            else:
                # Fallback if the GIF is invalid or not found
                raise Exception("Invalid or missing spinner.gif")
        except Exception:
            # Styled text fallback for when the GIF fails
            self.spinner.setText("<b style='color:white'>AI is generating...</b>") 
            
        self.spinner.hide()
        chat_lay.addWidget(self.spinner)

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Type your question here...")
        self.input_box.setFixedHeight(70)
        self.input_box.setStyleSheet("background-color: white; color: #0b3d91; border-radius: 8px; padding: 8px; font-size: 14px;")
        self.input_box.installEventFilter(self)
        chat_lay.addWidget(self.input_box, stretch=1)

        content.addWidget(chat_frame, stretch=1)

        # ---------- RIGHT: notes ----------
        notes_frame = QFrame()
        notes_frame.setStyleSheet("background-color: #e6e6e6; border-radius: 10px; padding: 8px;")
        notes_lay = QVBoxLayout(notes_frame)

        notes_title = QLabel("Notes")
        notes_title.setAlignment(Qt.AlignCenter)
        notes_title.setStyleSheet(f"font-size: 16px; font-weight: bold; margin: 6px; color: {primary};")
        notes_lay.addWidget(notes_title)

        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Type your notes here...")
        self.notes_edit.setStyleSheet("background-color: white; color: #0b3d91; border-radius: 8px; padding: 8px; font-size: 14px;")
        notes_lay.addWidget(self.notes_edit)

        content.addWidget(notes_frame, stretch=1)

        main.addLayout(content)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton { background-color: #4CAF50; color: white; border: none; padding: 10px 20px;
                          font-size: 14px; font-weight: bold; border-radius: 8px; margin: 10px; }
            QPushButton:hover { background-color: #45a049; }
        """)
        close_btn.clicked.connect(self.close)
        main.addWidget(close_btn, alignment=Qt.AlignRight)

        self.setLayout(main)

        start = self.lesson.get("start_prompt", "")
        if start:
            self.append_system_and_stream(start)

    # ------------------------------------------------------------------
    def eventFilter(self, obj, event):
        if obj == self.input_box and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if event.modifiers() == Qt.ShiftModifier:
                    return False
                else:
                    self._on_user_send()
                    return True
        return super().eventFilter(obj, event)

    # ------------------------------------------------------------------
    def _on_user_send(self):
        txt = self.input_box.toPlainText().strip()
        if not txt:
            return
        self.chat_display.append(f"<b>You:</b> {txt}\n")
        self.input_box.clear()
        self.append_and_stream("<b>AI:</b> ", txt)

    # ------------------------------------------------------------------
    # Only called once on window startup
    def append_system_and_stream(self, prompt_text: str):
        self.append_and_stream("<b>AI:</b> ", prompt_text)

    # ------------------------------------------------------------------
    def append_and_stream(self, prefix: str, prompt: str):
        self.spinner.show() # Show the spinner when starting the thread
        self.chat_display.append(prefix)
        QApplication.processEvents()

        worker = AIWorker(prompt)
        worker.signals.finished.connect(self._display_incremental)
        worker.signals.error.connect(lambda r: self._display_incremental(r))
        
        # Keep a reference to prevent garbage collection while the thread runs
        self._current_worker = worker 
        
        worker.run() # 🎯 RUN THE WORKER IN A NEW THREAD

    # ------------------------------------------------------------------
    def _display_incremental(self, full_text: Optional[str], chunk: int = 40, delay: int = 30):
        # Clear the worker reference once done
        if self._current_worker:
            del self._current_worker
            self._current_worker = None
            
        self.spinner.hide() # Hide the spinner when the thread returns
        
        if full_text is None:
            self.chat_display.append("<i style='color:red'>API error – check key/network</i>\n")
            return

        idx = 0
        vertical_scroll_bar: QScrollBar = self.chat_display.verticalScrollBar()

        def step():
            nonlocal idx
            if idx >= len(full_text):
                self.chat_display.append("\n") 
                
                if not self.challenge_printed:
                    challenge = self.lesson.get("challenge", "")
                    if challenge:
                        self.chat_display.append(f"<b>Challenge:</b> {challenge}\n")
                        self.challenge_printed = True 
                
                return

            end = min(idx + chunk, len(full_text))
            piece = full_text[idx:end]
            cur = self.chat_display.textCursor()
            cur.movePosition(QTextCursor.MoveOperation.End) 
            cur.insertText(piece)
            vertical_scroll_bar.setValue(vertical_scroll_bar.maximum())
            idx = end
            QTimer.singleShot(delay, step)

        QTimer.singleShot(0, step)