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
        left_layout.addStretch()  # Push everything to top

        # Right side - Vertical column (dark blue background) with a light-grey prompt box at the bottom
        right_layout = QVBoxLayout()
        right_widget = QFrame()
        right_widget.setLayout(right_layout)
        # Fill the right column with dark blue; child widgets will override their own colors where needed
        right_widget.setStyleSheet(f"background-color: {primary_text_color}; border-radius: 10px; padding: 8px;")
        right_widget.setFixedWidth(240)

        right_title = QLabel("Menu")
        right_title.setAlignment(Qt.AlignCenter)
        # Menu title should be white to contrast with dark blue background
        right_title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px; padding: 6px; color: white;")
        right_layout.addWidget(right_title)

        # Add some placeholder menu items
        menu_items = ["Profile", "Settings", "History", "Help"]
        for item in menu_items:
            menu_btn = QPushButton(item)
            # Buttons on the dark blue column should use white text and subtle hover
            menu_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    padding: 10px;
                    text-align: left;
                    font-size: 14px;
                    color: white;
                }
                QPushButton:hover {
                    background-color: rgba(255,255,255,0.06);
                }
            """)
            right_layout.addWidget(menu_btn)

        # Push the prompt box to the bottom
        right_layout.addStretch()

        # Light grey prompt box at the bottom of the right column
        prompt_box = QFrame()
        prompt_box.setStyleSheet("background-color: #e6e6e6; border-radius: 8px; padding: 8px;")
        prompt_box.setFixedHeight(120)
        prompt_layout = QVBoxLayout()
        prompt_box.setLayout(prompt_layout)

        prompt_label = QLabel("Message")
        prompt_label.setStyleSheet(f"color: {primary_text_color}; font-weight: bold; margin-bottom: 6px;")
        prompt_layout.addWidget(prompt_label)

        prompt_input = QTextEdit()
        prompt_input.setPlaceholderText("Type your message here...")
        # Ensure text entered into the prompt is dark blue to match the app text
        prompt_input.setStyleSheet(f"background-color: #ffffff; color: {primary_text_color}; border: 1px solid #dcdcdc; border-radius: 6px;")
        prompt_layout.addWidget(prompt_input)

        right_layout.addWidget(prompt_box)

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
