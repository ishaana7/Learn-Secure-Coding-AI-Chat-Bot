import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QTextEdit,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
from lesson_window import LessonWindow


class ProgressCircle(QWidget):
    def __init__(self, progress=0.0):
        super().__init__()
        self.progress = progress  # 0.0 to 1.0
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
            painter.setPen(QPen(QColor(34, 139, 34), 3))  # Forest green
            start_angle = 90 * 16  # Start from top
            span_angle = -int(360 * self.progress * 16)
            painter.drawArc(center.x() - radius, center.y() - radius, radius * 2, radius * 2, start_angle, span_angle)


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Secure Learning Chatbox - Dashboard")
        self.setFixedSize(800, 600)
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

        circle1 = ProgressCircle(1.0)
        circle2 = ProgressCircle(0.5)
        circle3 = ProgressCircle(0.25)
        circle4 = ProgressCircle(0.0)

        for circle in [circle1, circle2, circle3, circle4]:
            circles_layout.addWidget(circle)

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

        # Continue Learning button (keeps the dashboard title)
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

        # Add progress section to left layout
        left_layout.addLayout(progress_layout)

    # Keep the Continue button at its default size (do not force width)

        # Create a centered container that holds the Continue button and the lesson boxes
        center_container = QFrame()
        center_layout = QVBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(12)
        center_layout.setAlignment(Qt.AlignHCenter)
        center_container.setLayout(center_layout)

        # Put the continue button centered above the lesson boxes
        center_layout.addWidget(continue_btn, alignment=Qt.AlignHCenter)

        # --- Lessons boxes section ---
        lessons_layout = QHBoxLayout()
        # Increased spacing to avoid overlap (reduce a bit so all boxes fit)
        lessons_layout.setSpacing(24)
        # Remove outer margins so the entire group can be centered under the button
        lessons_layout.setContentsMargins(0, 12, 0, 12)

        # Create 4 labelled lesson boxes (plain centered text, transparent background, semi-transparent borders)
        lesson_titles = ["Input Validation", "Auth & Sessions", "Access Control", "Error Handling"]
        # semi-transparent border color (rgba of primary text color)
        semi_border = "rgba(11,61,145,0.55)"
        for title in lesson_titles:
            box = QFrame()
            # keep boxes compact (slightly narrower so all boxes fit)
            box.setFixedSize(90, 50)
            box.setStyleSheet(
                f"background-color: transparent;"
                f"border: 2px solid {semi_border};"
                f"border-radius: 8px;"
            )
            b_layout = QVBoxLayout()
            b_layout.setContentsMargins(4, 0, 4, 0)
            b_layout.setAlignment(Qt.AlignCenter)

            # Plain label (not a text box) centered inside the frame
            lbl = QLabel(title)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"color: {primary_text_color}; font-weight: 600; font-size: 13px; background: transparent;")
            b_layout.addWidget(lbl)
            box.setLayout(b_layout)
            lessons_layout.addWidget(box, alignment=Qt.AlignCenter)

        # Wrap the lessons_layout into a frame so it can be centered as a single widget
        lessons_frame = QFrame()
        lessons_frame.setLayout(lessons_layout)
        lessons_frame.setStyleSheet("background: transparent;")
        # Let the lessons_frame size to its contents so it centers naturally under the button
        center_layout.addWidget(lessons_frame, alignment=Qt.AlignCenter)

        # Add the center container (button above boxes) into the left layout, centered
        left_layout.addWidget(center_container, alignment=Qt.AlignHCenter)
        left_layout.addStretch()

        # --- Right side ---
        right_layout = QVBoxLayout()
        right_widget = QFrame()
        right_widget.setLayout(right_layout)
        right_widget.setStyleSheet(f"background-color: {primary_text_color}; border-radius: 10px; padding: 8px;")
        right_widget.setFixedWidth(240)
        # Heading at top of right column
        right_title = QLabel("AI Chatbox")
        right_title.setAlignment(Qt.AlignCenter)
        right_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold; margin: 6px;")
        right_layout.addWidget(right_title)
        right_layout.addStretch()

        # Interactive multi-line text area at the bottom for notes / typing
        notes_edit = QTextEdit()
        notes_edit.setPlaceholderText("Type your notes or chat here...")
        notes_edit.setFixedHeight(120)
        notes_edit.setStyleSheet(
            "background-color: white; color: #0b3d91; border-radius: 8px; padding: 8px;"
        )
        # Add at the bottom (after the stretch) so it stays anchored to the bottom
        right_layout.addWidget(notes_edit, alignment=Qt.AlignBottom)

        # Combine sides
        main_layout.addWidget(left_widget, stretch=3)
        main_layout.addWidget(right_widget, stretch=1)
        self.setLayout(main_layout)

    def continue_learning(self):
        # Open a lesson window. Keep a reference so it isn't garbage-collected.
        # Use the lesson title 'Input Handling' inside the lesson window
        lesson_title = "Input Handling"
        self.lesson_win = LessonWindow(lesson_title)
        self.lesson_win.show()


def main():
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
