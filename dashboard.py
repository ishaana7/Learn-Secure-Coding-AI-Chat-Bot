import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QBrush, QColor


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

        # Continue Learning Button
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

        # Add everything above to left layout
        left_layout.addLayout(progress_layout)
        left_layout.addWidget(continue_btn, alignment=Qt.AlignCenter)

        # --- Lessons boxes section ---
        lessons_layout = QHBoxLayout()
        # Increased spacing to avoid overlap
        lessons_layout.setSpacing(56)
        # Larger outer margins for clearer separation
        lessons_layout.setContentsMargins(24, 12, 24, 12)

        # Create 4 empty boxes
        for _ in range(4):
            box = QFrame()
            # make boxes a bit smaller
            box.setFixedSize(100, 50)
            box.setStyleSheet(
                f"background-color: transparent;"
                f"border: 2px solid {primary_text_color};"
                f"border-radius: 8px;"
            )
            lessons_layout.addWidget(box, alignment=Qt.AlignCenter)

        left_layout.addSpacing(12)
        left_layout.addLayout(lessons_layout)
        left_layout.addStretch()

        # --- Right side ---
        right_layout = QVBoxLayout()
        right_widget = QFrame()
        right_widget.setLayout(right_layout)
        right_widget.setStyleSheet(f"background-color: {primary_text_color}; border-radius: 10px; padding: 8px;")
        right_widget.setFixedWidth(240)
        right_layout.addStretch()

        # Combine sides
        main_layout.addWidget(left_widget, stretch=3)
        main_layout.addWidget(right_widget, stretch=1)
        self.setLayout(main_layout)

    def continue_learning(self):
        print("Continue Learning clicked!")


def main():
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
