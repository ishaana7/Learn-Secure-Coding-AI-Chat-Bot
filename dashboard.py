import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QLineEdit,
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
        
        # Draw outer circle (background)
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
            span_angle = -int(360 * self.progress * 16)  # Negative for clockwise
            painter.drawArc(center.x() - radius, center.y() - radius, radius * 2, radius * 2, start_angle, span_angle)

class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Secure Learning Chatbox - Dashboard")
        self.setFixedSize(800, 600)
        # Set main window background to light grey
        self.setStyleSheet("background-color: #e6e6e6;")
        # We'll use dark blue (#0b3d91) for primary text where needed
        primary_text_color = "#0b3d91"

        # Main horizontal layout
        main_layout = QHBoxLayout()

        # Left side - Progress and Continue Learning
        left_layout = QVBoxLayout()
        left_widget = QFrame()
        left_widget.setLayout(left_layout)
        left_widget.setStyleSheet("background-color: #e6e6e6; border-radius: 10px; padding: 12px;")

        # Progress circles section
        progress_layout = QVBoxLayout()
        progress_title = QLabel("Learning Progress")
        progress_title.setAlignment(Qt.AlignCenter)
        # Dark blue title text
        progress_title.setStyleSheet(f"font-size: 18px; font-weight: bold; margin: 20px; color: {primary_text_color};")
        progress_layout.addWidget(progress_title)

        # Create progress circles with different fill levels
        circles_layout = QHBoxLayout()
        circles_layout.setAlignment(Qt.AlignCenter)

        # Circle 1 - Completed (100%)
        circle1 = ProgressCircle(1.0)
        circles_layout.addWidget(circle1)

        # Circle 2 - Half filled (50%)
        circle2 = ProgressCircle(0.5)
        circles_layout.addWidget(circle2)

        # Circle 3 - Quarter filled (25%)
        circle3 = ProgressCircle(0.25)
        circles_layout.addWidget(circle3)

        # Circle 4 - Empty (0%)
        circle4 = ProgressCircle(0.0)
        circles_layout.addWidget(circle4)

        progress_layout.addLayout(circles_layout)

        # Labels for progress stages
        labels_layout = QHBoxLayout()
        labels_layout.setAlignment(Qt.AlignCenter)

        labels = ["Complete", "In Progress", "Started", "Not Started"]
        for label_text in labels:
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter)
            # Make progress labels dark blue to match overall text
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

        # Add everything to left layout
        left_layout.addLayout(progress_layout)
        left_layout.addWidget(continue_btn, alignment=Qt.AlignCenter)

        # Lessons boxes under the Continue Learning button
        lessons_layout = QHBoxLayout()
        # Increase spacing so boxes appear as separate entities
        lessons_layout.setSpacing(36)
        # Add outer margins around the whole lessons row for extra separation
        lessons_layout.setContentsMargins(12, 12, 12, 12)
        lesson_names = ["Loops", "Conditionals", "Functions", "Data Structures"]
        for name in lesson_names:
            # Transparent wrapper to provide outer margin (so frames don't touch or show connecting lines)
            wrapper = QFrame()
            wrapper.setStyleSheet("background-color: transparent;")
            wrapper_layout = QVBoxLayout()
            # outer margins create visible separation between lesson frames
            wrapper_layout.setContentsMargins(10, 0, 10, 0)
            wrapper.setLayout(wrapper_layout)

            # Single frame per lesson with full border
            lesson_frame = QFrame()
            lesson_frame.setFixedSize(170, 70)
            lesson_frame.setStyleSheet(
                f"background-color: transparent;"
                f"border-left: 2px solid {primary_text_color};"
                f"border-top: 2px solid {primary_text_color};"
                f"border-bottom: 2px solid {primary_text_color};"
                f"border-right: 0px solid transparent;"
                f"border-top-left-radius: 8px;"
                f"border-bottom-left-radius: 8px;"
            )
            lf_layout = QVBoxLayout()
            lf_layout.setContentsMargins(8, 4, 8, 4)
            lbl = QLabel(name)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"color: {primary_text_color}; font-weight: bold;")
            lf_layout.addWidget(lbl)
            lesson_frame.setLayout(lf_layout)

            # Inner container to hold the lesson frame and a thin vertical line to 'finish' the border
            inner = QFrame()
            inner_layout = QHBoxLayout()
            inner_layout.setContentsMargins(0, 0, 0, 0)
            inner_layout.setSpacing(0)
            # vertical line to the right of the box (2px) matching the primary color
            vline = QFrame()
            vline.setFixedWidth(2)
            vline.setFixedHeight(70)
            vline.setStyleSheet(f"background-color: {primary_text_color}; border: none; border-top-right-radius: 8px; border-bottom-right-radius: 8px;")

            inner_layout.addWidget(lesson_frame)
            inner_layout.addWidget(vline)
            inner.setLayout(inner_layout)

            wrapper_layout.addWidget(inner, alignment=Qt.AlignCenter)
            lessons_layout.addWidget(wrapper, alignment=Qt.AlignCenter)

        # Add spacing to visually separate from the button (approx same distance as circles above)
        left_layout.addSpacing(12)
        left_layout.addLayout(lessons_layout)
        left_layout.addStretch()  # Push everything to top

        # Right side - Vertical column (dark blue background) with a light-grey prompt box at the bottom
        right_layout = QVBoxLayout()
        right_widget = QFrame()
        right_widget.setLayout(right_layout)
        # Fill the right column with dark blue; child widgets will override their own colors where needed
        right_widget.setStyleSheet(f"background-color: {primary_text_color}; border-radius: 10px; padding: 8px;")
        right_widget.setFixedWidth(240)

        # Right column intentionally left minimal (visual accent only)
        # You can add widgets here later if needed.
        right_layout.addStretch()

        # Add both sides to main layout
        main_layout.addWidget(left_widget, stretch=3)  # Left side takes more space
        main_layout.addWidget(right_widget, stretch=1)  # Right side smaller

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
