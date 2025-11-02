# login.py
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from dashboard import DashboardWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure Learning Chatbox")
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()

        title = QLabel("Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        u_layout = QHBoxLayout()
        u_label = QLabel("Username:")
        u_label.setFixedWidth(80)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        u_layout.addWidget(u_label)
        u_layout.addWidget(self.username_input)
        layout.addLayout(u_layout)

        p_layout = QHBoxLayout()
        p_label = QLabel("Password:")
        p_label.setFixedWidth(80)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        p_layout.addWidget(p_label)
        p_layout.addWidget(self.password_input)
        layout.addLayout(p_layout)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        self.setLayout(layout)

    def handle_login(self):
        if self.username_input.text() and self.password_input.text():
            self.hide()
            self.dashboard = DashboardWindow()
            self.dashboard.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())
