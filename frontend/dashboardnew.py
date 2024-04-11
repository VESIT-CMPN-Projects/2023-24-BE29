import sys
import sqlite3
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont ,QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QMessageBox, \
    QMainWindow, QHBoxLayout, QStackedWidget, QFormLayout, QTextEdit, QFileDialog, QSizePolicy

class DashboardPage(QMainWindow):
    submit_from_signal = pyqtSignal()
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



#     def create_form_page(self):
#         page_widget = QWebEngineView()
#         # Added now
#         # web_bridge = WebBridge(self)

#         # Install the URL scheme handler
#         # handler = QWebEngineUrlSchemeHandler()
#         # handler.setRequestInterceptionEnabled(True)
#         # handler.setBaseUrl(QUrl("pyweb://"))
#         # handler.interceptRequest.connect(web_bridge.intercept_request)
#         # page_widget.page().profile().installUrlSchemeHandler(b"pyweb", WebBridge())

#         page_widget.setHtml("""
              
#                 <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Form Page</title>
#     <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
#     <style>
#         /* Custom styles */
#         .container {
#             max-width: 500px; /* Limit form width */
#             margin: auto; /* Center align container */
#             padding-top: 50px; /* Add space at the top */
#         }
#         .form-group {
#             margin-bottom: 20px; /* Add space between form fields */
#         }
#         .input-group-append {
#             margin-left: -1px; /* Adjust margin for the append button */
#         }
#         .btn-submit {
#             width: 100%; /* Make submit button full-width */
#         }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <h1 class="text-center mb-4">Fill your car details</h1>
#         <form>
#             <div class="form-group">
#                 <label for="name">Name:</label>
#                 <input type="text" class="form-control" id="name" placeholder="Enter name">
#             </div>
#             <div class="form-group">
#                 <label for="number_plate">Number Plate:</label>
#                 <input type="text" class="form-control" id="number_plate" placeholder="Enter number plate">
#             </div>
#             <div class="form-group">
#                 <label for="color">Color:</label>
#                 <input type="text" class="form-control" id="color" placeholder="Enter color">
#             </div>
#             <div class="form-group">
#                 <label for="model">Model:</label>
#                 <input type="text" class="form-control" id="model" placeholder="Enter model">
#             </div>
#             <div class="form-group">
#                 <label for="image_path">Image:</label>
#                 <div class="input-group">
#                     <input type="text" class="form-control" id="image_path" placeholder="Image path">
#                     <div class="input-group-append">
#                         <button type="button" class="btn btn-primary">Browse</button>
#                     </div>
#                 </div>
#             </div>
#             <button type="submit" onclick="submit_form()" class="btn btn-primary btn-submit">Submit</button>
#                                 <script>
#                 function submit_form() {
#                     var name = document.getElementById("name").value;
#                     var number_plate = document.getElementById("number_plate").value;
#                     var color = document.getElementById("color").value;
#                     var model = document.getElementById("model").value;
#                     var image_path = document.getElementById("image_path").value;
#                     console.log(name);
#                     // pyweb.submit_form(name, number_plate, color, model, image_path);
#                 }
#             </script>
#         </form>
#     </div>
# </body>
# </html>
#             """)
#         return page_widget