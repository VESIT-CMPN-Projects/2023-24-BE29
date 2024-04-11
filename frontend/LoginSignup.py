import sys
import sqlite3
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont ,QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QMessageBox, \
    QMainWindow, QHBoxLayout, QStackedWidget, QFormLayout, QTextEdit, QFileDialog, QSizePolicy

class LoginSignupPage(QWidget):
    login_successful = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login / Signup')
        self.setGeometry(0, 0, 1000, 700)
        self.setStyleSheet("background-color: #E4E8F4;")

        self.create_table()

        self.stack = QStackedWidget()
        self.login_widget = QWidget()
        self.signup_widget = QWidget()

        self.init_login_ui()
        self.init_signup_ui()

        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.signup_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)

        self.setLayout(layout)

    def create_table(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE,
                      password TEXT)''')
        conn.commit()
        conn.close()

    def init_login_ui(self):
        layout = QVBoxLayout()

        logo_container = QHBoxLayout()
        logo_label1 = QLabel()
        logo_pixmap1 = QPixmap("../assets/images/VESIT_logo.png").scaledToWidth(70)  
        logo_label1.setPixmap(logo_pixmap1)
        logo_container.addWidget(logo_label1)

        logo_label2 = QLabel()
        logo_pixmap2 = QPixmap("../assets/images/TIFR_logo.png").scaledToWidth(70)  
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

    def init_signup_ui(self):
        layout = QVBoxLayout()

        logo_container = QHBoxLayout()
        logo_label1 = QLabel()
        logo_pixmap1 = QPixmap("../assets/images/VESIT_logo").scaledToWidth(70)  
        logo_label1.setPixmap(logo_pixmap1)
        logo_container.addWidget(logo_label1)

        logo_label2 = QLabel()
        logo_pixmap2 = QPixmap("../assets/images/TIFR_logo.png").scaledToWidth(70)  
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

    def login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()

        if not (username and password):
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        result = c.fetchone()
        conn.close()

        if result:
            self.login_successful.emit(username)
            QMessageBox.information(self, "Success", "Login Successful!")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")

    def signup(self):
        username = self.signup_username.text().strip()
        password = self.signup_password.text().strip()

        if not (username and password):
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            QMessageBox.information(self, "Success", f"Signup Successful!\nUsername: {username}\nPassword: {password}")
            self.show_login()  # Switch back to the login page
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists. Please choose a different username.")
        conn.close()



    def show_signup(self):
        self.stack.setCurrentIndex(1)

    def show_login(self):
        self.stack.setCurrentIndex(0)





class DashboardPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1000, 700)

        self.setWindowTitle('Dashboard')
        self.setStyleSheet("background-color: #E4E8F4;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_layout = QHBoxLayout()
        central_widget.setLayout(central_layout)

        # Sidebar layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)
        central_layout.addLayout(sidebar_layout)

        # Hamburger menu button
        self.menu_button = QPushButton('\u2630')
        self.menu_button.setStyleSheet("font-size: 24px;")
        self.menu_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sidebar_layout.addWidget(self.menu_button)

        # Navigation options (initially hidden)
        self.options_widget = QWidget()
        self.options_layout = QVBoxLayout(self.options_widget)
        self.options_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.addWidget(self.options_widget)
        self.options_widget.setVisible(False)

        # Add options
        self.add_option("Home", "home.png")
        self.add_option("Notification", "notification.png")
        self.add_option("Contact Us", "contact.png")

        # Stacked widget for main content
        self.stacked_widget = QStackedWidget()
        central_layout.addWidget(self.stacked_widget)

        # Form button (centered)
        self.form_button = QPushButton("Form")
        self.form_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.form_button.setStyleSheet("font-size: 16px;")
        central_layout.addWidget(self.form_button, alignment=Qt.AlignHCenter)

        # Connect menu button click event to toggle sidebar visibility
        self.menu_button.clicked.connect(self.toggle_sidebar_visibility)

        # Connect form button click event to show_form function
        self.form_button.clicked.connect(self.show_form)

    def show_finding_car_page(self):
        page_widget = QWidget()
        layout = QVBoxLayout()
        text_label = QLabel("Sit back and relax, we are finding your car...")
        text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(text_label)
        page_widget.setLayout(layout)
        self.stacked_widget.addWidget(page_widget)
        self.stacked_widget.setCurrentWidget(page_widget)

    def create_form_page(self):
        page_widget = QWidget()
        layout = QFormLayout()

        name_edit = QLineEdit()
        name_edit.setPlaceholderText("Enter name")
        layout.addRow(QLabel("Name:"), name_edit)

        number_plate_edit = QLineEdit()
        number_plate_edit.setPlaceholderText("Enter number plate")
        layout.addRow(QLabel("Number Plate:"), number_plate_edit)

        color_edit = QLineEdit()
        color_edit.setPlaceholderText("Enter color")
        layout.addRow(QLabel("Color:"), color_edit)

        model_edit = QLineEdit()
        model_edit.setPlaceholderText("Enter model")
        layout.addRow(QLabel("Model:"), model_edit)

        image_edit = QLineEdit()
        image_edit.setPlaceholderText("Image path")
        image_button = QPushButton("Browse")
        image_button.clicked.connect(lambda: self.get_image_path(image_edit))
        layout.addRow(QLabel("Image:"), image_edit)
        layout.addRow(image_button)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.submit_form(name_edit.text(), number_plate_edit.text(),
                                                                color_edit.text(), model_edit.text(),
                                                                image_edit.text()))
        submit_button.clicked.connect(self.show_finding_car_page)  # Connect to show finding car page
        layout.addRow(submit_button)

        page_widget.setLayout(layout)
        return page_widget

    def clear_form(self):
        # Clear all form fields
        for widget in self.stacked_widget.currentWidget().findChildren(QLineEdit):
            widget.clear()

    def show_form(self):
        # Hide the form button
        self.form_button.hide()

        # Remove previous widgets from stacked widget
        for i in reversed(range(self.stacked_widget.count())):
            self.stacked_widget.widget(i).deleteLater()

        # Create and show the form widget
        form_widget = self.create_form_page()
        self.stacked_widget.addWidget(form_widget)

    def toggle_sidebar_visibility(self):
        # Toggle sidebar visibility
        is_visible = not self.options_widget.isVisible()
        self.options_widget.setVisible(is_visible)

    def add_option(self, text, icon_path):
        option_button = QPushButton(text)
        option_button.setIcon(QIcon(icon_path))
        option_button.setIconSize(QSize(24, 24))
        option_button.setFixedSize(200, 40)
        self.options_layout.addWidget(option_button)

    def get_image_path(self, image_edit):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if filename:
            image_edit.setText(filename)

    def submit_form(self, name, number_plate, color, model, image_path):
        if not (name and number_plate and color and model):
            QMessageBox.warning(self, "Error", "All fields are mandatory")
            return

        try:
            # Connect to the database
            conn = sqlite3.connect('car_data.db')
            c = conn.cursor()

            # Print the database schema for debugging
            c.execute("PRAGMA table_info(cars)")
            print("Table Schema:", c.fetchall())

            # Save data to database
            c.execute('INSERT INTO cars (name, number_plate, color, model, image_path) VALUES (?, ?, ?, ?, ?)',
                      (name, number_plate, color, model, image_path))
            self.form_button.show()

            conn.commit()
            conn.close()

            # Clear the form fields
            self.clear_form()

            # Create and show the new page with the message
            self.show_finding_car_page()

            # Remove the form widget from stacked widget
            self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

        except sqlite3.Error as e:
            print("Error occurred while inserting data into database:", e)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    login_signup_page = LoginSignupPage()
    dashboard_page = DashboardPage()

    login_signup_page.login_successful.connect(dashboard_page.show)

    login_signup_page.show()

    sys.exit(app.exec_())