import sys
import sqlite3
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, \
    QMessageBox, QMainWindow, QHBoxLayout, QStackedWidget, QFormLayout, QTextEdit, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QStackedWidget, QSizePolicy, QLabel, QLineEdit, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


class LoginSignupPage(QWidget):
    login_successful = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login / Signup')
        self.setGeometry(100, 100, 400, 300)

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
                      username TEXT,
                      password TEXT)''')
        conn.commit()
        conn.close()

    def init_login_ui(self):
        layout = QVBoxLayout()

        self.login_username = QLineEdit()
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        login_button = QPushButton("Login")
        signup_button = QPushButton("Switch to Signup")

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.login_username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.login_password)
        layout.addWidget(login_button)
        layout.addWidget(signup_button)

        self.login_widget.setLayout(layout)

        login_button.clicked.connect(self.login)
        signup_button.clicked.connect(self.show_signup)

    def init_signup_ui(self):
        layout = QVBoxLayout()

        self.signup_username = QLineEdit()
        self.signup_password = QLineEdit()
        self.signup_password.setEchoMode(QLineEdit.Password)
        signup_button = QPushButton("Signup")
        login_button = QPushButton("Switch to Login")

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.signup_username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.signup_password)
        layout.addWidget(signup_button)
        layout.addWidget(login_button)

        self.signup_widget.setLayout(layout)

        signup_button.clicked.connect(self.signup)
        login_button.clicked.connect(self.show_login)

    def login(self):
        username = self.login_username.text()
        password = self.login_password.text()

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        result = c.fetchone()
        conn.close()

        if result:
            self.login_successful.emit(username)
            QMessageBox.information(self, "Success", "Login Successful!")
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")

    def signup(self):
        username = self.signup_username.text()
        password = self.signup_password.text()

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", f"Signup Successful!\nUsername: {username}\nPassword: {password}")

    def show_signup(self):
        self.stack.setCurrentIndex(1)

    def show_login(self):
        self.stack.setCurrentIndex(0)




from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QStackedWidget, QSizePolicy, QLabel, QLineEdit, QTextEdit, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import sqlite3

class DashboardPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dashboard')

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

    def show_form(self):
        # Clear stacked widget
        self.stacked_widget.clear()

        # Create form widget
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        self.stacked_widget.addWidget(form_widget)

        # Form fields
        name_label = QLabel("Name:")
        name_edit = QLineEdit()
        form_layout.addWidget(name_label)
        form_layout.addWidget(name_edit)

        numberplate_label = QLabel("Number Plate:")
        numberplate_edit = QLineEdit()
        form_layout.addWidget(numberplate_label)
        form_layout.addWidget(numberplate_edit)

        color_label = QLabel("Color:")
        color_edit = QLineEdit()
        form_layout.addWidget(color_label)
        form_layout.addWidget(color_edit)

        model_label = QLabel("Model:")
        model_edit = QLineEdit()
        form_layout.addWidget(model_label)
        form_layout.addWidget(model_edit)

        image_label = QLabel("Image:")
        self.image_edit = QLineEdit()
        image_button = QPushButton("Select Image")
        image_button.clicked.connect(self.select_image)
        form_layout.addWidget(image_label)
        form_layout.addWidget(self.image_edit)
        form_layout.addWidget(image_button)

        # Submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.submit_form(name_edit.text(), numberplate_edit.text(), color_edit.text(), model_edit.text()))
        form_layout.addWidget(submit_button)

    def select_image(self):
        # Open file dialog to select image
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select Image', '', 'Image files (*.jpg *.png)')
        if file_path:
            self.image_edit.setText(file_path)

    def submit_form(self, name, numberplate, color, model):
        # Store form data in the car database
        try:
            conn = sqlite3.connect('car.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS car (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT,
                         numberplate TEXT,
                         color TEXT,
                         model TEXT,
                         image BLOB)''')
            conn.commit()

            with open(self.image_edit.text(), 'rb') as f:
                image_data = f.read()

            c.execute("INSERT INTO car (name, numberplate, color, model, image) VALUES (?, ?, ?, ?, ?)",
                      (name, numberplate, color, model, image_data))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Data stored successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error occurred while storing data: {str(e)}")





    def setStyleForButton(self, button):
        button.setStyleSheet("background-color: #87CEEB; color: white; padding: 10px; border-radius: 5px;")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        print("Button clicked!")

    def createPage1(self):
        page_widget = QWidget()
        return page_widget

    def createPage2(self):
        page_widget = QWidget()
        return page_widget

    def createPage3(self):
        page_widget = QWidget()
        return page_widget

    def createFormPage(self):
        
        

    # Connect to the database
        conn = sqlite3.connect('car_data.db')
        c = conn.cursor()

        # Create the "cars" table if it does not already exist
        c.execute('''CREATE TABLE IF NOT EXISTS cars
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              number_plate TEXT,
              color TEXT,
              model TEXT,
              image_path TEXT)''')

        # Commit changes and close connection
        conn.commit()
        conn.close()


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
    
        # Create a horizontal layout for the image field and browse button
        image_layout = QHBoxLayout()
        image_layout.addWidget(image_edit)
        image_layout.addWidget(image_button)
        layout.addRow(QLabel("Image:"), image_layout)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.submit_form(name_edit.text(), number_plate_edit.text(),
                                                           color_edit.text(), model_edit.text(),
                                                           image_edit.text()))
        layout.addRow(submit_button)

        page_widget.setLayout(layout)
        return page_widget

    

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
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Sit back and relax, we are looking for your car :)")

            # Clear the form fields
            self.clear_form()
        except sqlite3.Error as e:
            print("Error occurred while inserting data into database:", e)



    def clear_form(self):
        # Clear all form fields
        for widget in self.stacked_widget.widget(3).findChildren(QLineEdit):
            widget.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    login_signup_page = LoginSignupPage()
    dashboard_page = DashboardPage()

    login_signup_page.login_successful.connect(dashboard_page.show)

    login_signup_page.show()

    sys.exit(app.exec_())

   