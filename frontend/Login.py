import sys
import sqlite3
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont ,QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QMessageBox, \
    QMainWindow, QHBoxLayout, QStackedWidget, QFormLayout, QTextEdit, QFileDialog, QSizePolicy

# from SignUp import SignUpPage
class LoginPage(QWidget):
    login_successful = pyqtSignal(str)
    show_signup_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Login')
        self.setGeometry(0, 0, 1000, 700)
        self.setStyleSheet("background-color: #E4E8F4;")

        # self.create_table()

        self.stack = QStackedWidget()
        self.login_widget = QWidget()
        # sign_up = SignUpPage()
        self.init_login_ui()

        self.stack.addWidget(self.login_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)

        self.setLayout(layout)

    def init_login_ui(self):
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
    
        heading_label = QLabel("Missing Substance Detection")
        heading_label.setAlignment(Qt.AlignCenter)
        heading_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(heading_label)

        login_container = QWidget()
        login_container.setStyleSheet("border:none; border-radius: 5px; width: 1%; margin: 0 auto;")
        login_container_layout = QVBoxLayout(login_container)
        login_container_layout.setAlignment(Qt.AlignCenter)

        self.login_username = QLineEdit()
        self.login_username.setStyleSheet("border:  1px solid gray; padding:10px;")
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setStyleSheet("border:  1px solid gray;padding:10px;")
        login_button = QPushButton("Login")
        signup_button = QPushButton("New user? Sign Up")
        self.login_username.setFixedWidth(450)
        self.login_password.setFixedWidth(450)

        login_button.setFixedWidth(150) 
        login_button.setStyleSheet("background-color: blue; color: white; border-radius: 5px; padding: 8px;")

        login_container_layout.addWidget(QLabel("Username:"))
        login_container_layout.addWidget(self.login_username)
        login_container_layout.addWidget(QLabel("Password:"))
        login_container_layout.addWidget(self.login_password)
        login_container_layout.addWidget(login_button)
        login_container_layout.addWidget(signup_button)

        layout.addWidget(login_container)
        layout.addStretch(1)

        login_button.clicked.connect(self.login)
        signup_button.clicked.connect(self.show_signup)

        self.login_widget.setLayout(layout)

    def login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()

        if not (username and password):
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        conn = sqlite3.connect('frontend/Databases/users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        result = c.fetchone()
        conn.close()
        self.login_successful.emit(username)
        self.close()

        if result == False:
            # self.login_successful.emit(username)
            # QMessageBox.information(self, "Success", "Login Successful!")
            QMessageBox.warning(self, "Error", "Invalid username or password.")
        # else:
        #     QMessageBox.warning(self, "Error", "Invalid username or password.")
        
    def show_signup(self):
        self.stack.setCurrentIndex(1)
        self.show_signup_signal.emit()
        self.close()
        print('Show Signup')
# if __name__ == '__main__':
#     app = QApplication(sys.argv)

#     login_page = LoginPage()


#     # login_page.login_successful.connect(dashboard_page.show)

#     login_page.show()

#     sys.exit(app.exec_())