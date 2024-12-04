import sys
import sqlite3
import qrcode
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


# Database setup
def setup_database():
    conn = sqlite3.connect("gate_pass.db")
    cursor = conn.cursor()
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS laptops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT,
        serial_number TEXT,
        qr_code_data TEXT,
        password TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT,
        number_plate TEXT,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()


# Main Window
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


# Register Laptop Window
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
        qr_code = qrcode.make(qr_data)
        qr_code.save("laptop_qr.png")

        pixmap = QPixmap("laptop_qr.png")
        self.qr_label.setPixmap(pixmap)

        conn = sqlite3.connect("gate_pass.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO laptops (member_id, serial_number, qr_code_data, password)
        VALUES (?, ?, ?, ?)
        """, (member_id, serial, qr_data, password))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Laptop registered and QR code generated!")

    def back_to_main(self):
        self.close()
        self.main_window = GatePassSystem()
        self.main_window.show()


# Register Car Window
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

        conn = sqlite3.connect("gate_pass.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO cars (member_id, number_plate, password)
        VALUES (?, ?, ?)
        """, (member_id, number_plate, password))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Car registered!")

    def back_to_main(self):
        self.close()
        self.main_window = GatePassSystem()
        self.main_window.show()


# Authenticate Exit Window
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
        self.qr_or_plate_input.setPlaceholderText("Enter QR Code Data or Number Plate")
        layout.addWidget(self.qr_or_plate_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

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

        conn = sqlite3.connect("gate_pass.db")
        cursor = conn.cursor()

        # Check laptops
        cursor.execute("""
        SELECT * FROM laptops WHERE qr_code_data=? AND password=?
        """, (input_data, password))
        laptop = cursor.fetchone()

        # Check cars
        cursor.execute("""
        SELECT * FROM cars WHERE number_plate=? AND password=?
        """, (input_data, password))
        car = cursor.fetchone()

        conn.close()

        if laptop:
            QMessageBox.information(self, "Success", "Laptop exit authenticated!")
        elif car:
            QMessageBox.information(self, "Success", "Car exit authenticated!")
        else:
            QMessageBox.warning(self, "Error", "Authentication failed!")

    def back_to_main(self):
        self.close()
        self.main_window = GatePassSystem()
        self.main_window.show()


if __name__ == "__main__":
    setup_database()
    app = QApplication(sys.argv)
    main_window = GatePassSystem()
    main_window.show()
    sys.exit(app.exec())
