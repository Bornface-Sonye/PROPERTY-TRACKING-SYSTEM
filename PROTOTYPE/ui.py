from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from qr_code import generate_qr_code
from database import register_laptop, register_car, authenticate_laptop, authenticate_car

class GatePassSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gate Pass System")
        self.setGeometry(300, 200, 500, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Choose an option:")
        layout.addWidget(self.label)

        self.register_laptop_button = QPushButton("Register Laptop")
        self.register_laptop_button.clicked.connect(self.register_laptop)
        layout.addWidget(self.register_laptop_button)

        self.register_car_button = QPushButton("Register Car")
        self.register_car_button.clicked.connect(self.register_car)
        layout.addWidget(self.register_car_button)

        self.authenticate_exit_button = QPushButton("Authenticate Exit")
        self.authenticate_exit_button.clicked.connect(self.authenticate_exit)
        layout.addWidget(self.authenticate_exit_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def register_laptop(self):
        self.close()
        self.registration_window = RegisterLaptopWindow()
        self.registration_window.show()

    def register_car(self):
        self.close()
        self.registration_window = RegisterCarWindow()
        self.registration_window.show()

    def authenticate_exit(self):
        self.close()
        self.auth_window = AuthenticateExitWindow()
        self.auth_window.show()

class RegisterLaptopWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register Laptop")
        self.setGeometry(300, 200, 400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("Register a Laptop")
        layout.addWidget(self.label)

        self.member_id_input = QLineEdit()
        self.member_id_input.setPlaceholderText("Enter Member ID")
        layout.addWidget(self.member_id_input)

        self.serial_input = QLineEdit()
        self.serial_input.setPlaceholderText("Enter Laptop Serial Number")
        layout.addWidget(self.serial_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_laptop)
        layout.addWidget(self.register_button)

        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.qr_label)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def register_laptop(self):
        member_id = self.member_id_input.text()
        serial = self.serial_input.text()
        password = self.password_input.text()

        if not (member_id and serial and password):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        qr_data = f"Laptop|Member:{member_id}|Serial:{serial}|Password:{password}"
        qr_code = generate_qr_code(qr_data)
        self.qr_label.setPixmap(qr_code)

        register_laptop(member_id, serial, qr_data, password)

        QMessageBox.information(self, "Success", "Laptop registered and QR code generated!")

    def back_to_main(self):
        self.close()
        self.main_window = GatePassSystem()
        self.main_window.show()

class RegisterCarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register Car")
        self.setGeometry(300, 200, 400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Register a Car")
        layout.addWidget(self.label)

        self.member_id_input = QLineEdit()
        self.member_id_input.setPlaceholderText("Enter Member ID")
        layout.addWidget(self.member_id_input)

        self.number_plate_input = QLineEdit()
        self.number_plate_input.setPlaceholderText("Enter Number Plate")
        layout.addWidget(self.number_plate_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_car)
        layout.addWidget(self.register_button)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def register_car(self):
        member_id = self.member_id_input.text()
        number_plate = self.number_plate_input.text()
        password = self.password_input.text()

        if not (member_id and number_plate and password):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        register_car(member_id, number_plate, password)

        QMessageBox.information(self, "Success", "Car registered!")

    def back_to_main(self):
        self.close()
        self.main_window = GatePassSystem()
        self.main_window.show()

class AuthenticateExitWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authenticate Exit")
        self.setGeometry(300, 200, 400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Authenticate Exit")
        layout.addWidget(self.label)

        self.qr_or_plate_input = QLineEdit()
        self.qr_or_plate_input.setPlaceholderText("Enter Number Plate (or Scan QR)")
        layout.addWidget(self.qr_or_plate_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.scan_button = QPushButton("Scan QR Code")
        self.scan_button.clicked.connect(self.scan_qr_code)
        layout.addWidget(self.scan_button)

        self.authenticate_button = QPushButton("Authenticate")
        self.authenticate_button.clicked.connect(self.authenticate)
        layout.addWidget(self.authenticate_button)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def authenticate(self):
        input_data = self.qr_or_plate_input.text()
        password = self.password_input.text()

        if input_data.startswith("Laptop"):
            laptop = authenticate_laptop(input_data, password)
            if laptop:
                QMessageBox.information(self, "Success", "Laptop Authenticated!")
            else:
                QMessageBox.warning(self, "Error", "Authentication Failed!")
        else:
            car = authenticate_car(input_data, password)
            if car:
                QMessageBox.information(self, "Success", "Car Authenticated!")
            else:
                QMessageBox.warning(self, "Error", "Authentication Failed!")

    def scan_qr_code(self):
        QMessageBox.information(self, "Scan QR Code", "Scan QR code functionality here!")

    def back_to_main(self):
        self.close()
        self.main_window = GatePassSystem()
        self.main_window.show()
