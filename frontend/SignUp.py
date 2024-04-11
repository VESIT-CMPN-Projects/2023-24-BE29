import sys
import sqlite3
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont ,QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QMessageBox, \
    QMainWindow, QHBoxLayout, QStackedWidget, QFormLayout, QTextEdit, QFileDialog, QSizePolicy


class SignUpPage(QWidget):
    show_login_signal = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Sign Up')
        self.setGeometry(0, 0, 1000, 700)
        self.setStyleSheet("background-color: #E4E8F4;")

        # self.create_table()

        self.stack = QStackedWidget()
        self.signup_widget = QWidget()

        

        self.init_signup_ui()

        self.stack.addWidget(self.signup_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)

        self.setLayout(layout)


    def create_table(self):
        conn = sqlite3.connect('Databases/users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE,
                      password TEXT)''')
        conn.commit()
        conn.close()
    def init_signup_ui(self):
        layout = QVBoxLayout()

        logo_container = QHBoxLayout()
        logo_label1 = QLabel()
        logo_pixmap1 = QPixmap("./assets/images/VESIT_logo.png").scaledToWidth(70)  
        logo_label1.setPixmap(logo_pixmap1)
        logo_container.addWidget(logo_label1)

        logo_label2 = QLabel()
        logo_pixmap2 = QPixmap("./assets/images/TIFR_logo.png").scaledToWidth(70)  
        logo_label2.setPixmap(logo_pixmap2)
        logo_container.addWidget(logo_label2)

        layout.addLayout(logo_container)
        logo_container.setAlignment(Qt.AlignCenter)
        # logo_container.addSpacing(30)
    
        heading_label = QLabel("Missing Substance Detection")
        heading_label.setAlignment(Qt.AlignCenter)
        heading_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(heading_label)


        signup_container = QWidget()
        signup_container.setStyleSheet("border: none; border-radius: 5px; width: 20%; margin: 0 auto;")
        signup_container_layout = QVBoxLayout(signup_container)
        signup_container_layout.setAlignment(Qt.AlignCenter)

        self.signup_username = QLineEdit()
        self.signup_username.setStyleSheet("border:  1px solid gray;")
        self.signup_password = QLineEdit()
        self.signup_password.setEchoMode(QLineEdit.Password)
        self.signup_password.setStyleSheet("border: 1px solid gray;")
        signup_button = QPushButton("Signup")

        signup_button.setFixedWidth(150) 
        signup_button.setStyleSheet("background-color: blue; color: white; border-radius: 5px; padding: 8px;") 

        signup_container_layout.addWidget(QLabel("Username:"))
        signup_container_layout.addWidget(self.signup_username)
        signup_container_layout.addWidget(QLabel("Password:"))
        signup_container_layout.addWidget(self.signup_password)
        signup_container_layout.addWidget(signup_button)

        layout.addWidget(signup_container)
        layout.addStretch(1)

        signup_button.clicked.connect(self.signup)

        self.signup_widget.setLayout(layout)

    def signup(self):
        username = self.signup_username.text().strip()
        password = self.signup_password.text().strip()

        if not (username and password):
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        conn = sqlite3.connect('Databases/users.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            QMessageBox.information(self, "Success", f"Signup Successful!\nUsername: {username}\nPassword: {password}")
            # self.show_login()  # Switch back to the login page
            self.show_login_signal.emit()
            self.close()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists. Please choose a different username.")
        conn.close()
        # self.login_page.stack.setCurrentIndex(0)
    def show_login(self):
        self.stack.setCurrentIndex(0)
