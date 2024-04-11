import sys
import sqlite3
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QUrl
from PyQt5.QtGui import QIcon, QFont ,QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QMessageBox, \
    QMainWindow, QHBoxLayout, QStackedWidget, QFormLayout, QTextEdit, QFileDialog, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView,QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtCore import QObject
# from PyQt5.QtWebEngineCore import QWebEngineUrlSchemeHandler
# from PyQt5.QtWebEngineWidgets import QWebEngineUrlSchemeHandler

class WebBridge(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def submit_form(self, name, number_plate, color,model, image_path):
        self.parent().submit_form(name, number_plate, color,model, image_path)

class DashboardPage(QMainWindow):
    submit_from_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1000, 700)
        self.setWindowTitle('Dashboard')
        self.setStyleSheet("background-color: #FFFFFF;")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_layout = QHBoxLayout()
        central_widget.setLayout(central_layout)


        # Load Bootstrap CSS file
        self.bootstrap_view = QWebEngineView()
        self.bootstrap_view.setUrl(QUrl.fromLocalFile('bootstrap.min.css'))  # Path to your bootstrap.min.css file
        self.bootstrap_view.hide()

        # Add Bootstrap view to central layout
        central_layout.addWidget(self.bootstrap_view)

        # Your existing code continues...

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
        

        # Add spacer for top padding
        layout.setVerticalSpacing(20)
        layout.SetFixedSize(10,4)

        name_edit = QLineEdit()
        # name_edit.setGeometry(200, 300,10,20)
        name_edit.setPlaceholderText("Enter name")
        name_edit.setStyleSheet('background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px;width: 200px; height: 300px; border-radius: 10px;padding:10px;') # Adjust border-radius value for desired roundness

        name_label = QLabel("Name:")
        name_label.setStyleSheet('color: black; font-size: 16px;')
        layout.addRow(name_label, name_edit)

        number_plate_edit = QLineEdit()
        number_plate_edit.setPlaceholderText("Enter number plate")
        number_plate_edit.setStyleSheet('background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px;width: 200px; height: 300px; border-radius: 10px;padding:10px;')

        layout.addRow(QLabel("Number Plate:"), number_plate_edit)

        color_edit = QLineEdit()
        color_edit.setPlaceholderText("Enter color")
        color_edit.setStyleSheet('background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px;width: 200px; height: 300px; border-radius: 10px;padding:10px;')
        layout.addRow(QLabel("Color:"), color_edit)

        model_edit = QLineEdit()
        model_edit.setPlaceholderText("Enter model")
        layout.addRow(QLabel("Model:"), model_edit)

        image_edit = QLineEdit()
        image_edit.setPlaceholderText("Image path")
        image_button = QPushButton("Browse")
        image_button.clicked.connect(lambda: self.get_image_path(image_edit))
        layout.addRow(QLabel("Image:"), image_edit)

        # Add horizontal spacer between image_edit and image_button
        hspacer_layout = QHBoxLayout()
        hspacer_layout.addWidget(image_button)
        hspacer_layout.addStretch(1)
        layout.addRow(hspacer_layout)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.submit_form(name_edit.text(), number_plate_edit.text(),
                                                                color_edit.text(), model_edit.text(),
                                                                image_edit.text()))
        submit_button.clicked.connect(self.show_finding_car_page)  # Connect to show finding car page
        layout.addRow(submit_button)

        # Add spacer for bottom padding
        layout.setVerticalSpacing(20)

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
            conn = sqlite3.connect('Frontend/Databases/car_data.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS cars (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT,
                         number_plate TEXT,
                         color TEXT,
                         model TEXT,
                         image BLOB)''')
            conn.commit()

            # Print the database schema for debugging
            c.execute("PRAGMA table_info(cars)")
            print("Table Schema:", c.fetchall())

            # Save data to database
            c.execute('INSERT INTO cars(name, number_plate, color, model, image) VALUES (?, ?, ?, ?, ?)',
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
        self.submit_from_signal.emit()






