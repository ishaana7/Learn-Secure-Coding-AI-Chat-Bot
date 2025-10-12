import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from dashboard import DashboardWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Secure Learning Chatbox")
        self.setFixedSize(300, 200)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Login title
        title = QLabel("Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Username section
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setFixedWidth(80)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # Password section
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setFixedWidth(80)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        self.setLayout(layout)
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        # Simple validation - just check if fields are not empty
        if username and password:
            print(f"Login successful for user: {username}")
            # Hide login window and show dashboard
            self.hide()
            self.dashboard = DashboardWindow()
            self.dashboard.show()
        else:
            print("Please enter both username and password")

def main():
    app = QApplication(sys.argv)
    
    window = LoginWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
