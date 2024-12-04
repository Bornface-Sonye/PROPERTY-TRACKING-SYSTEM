import sys
from PyQt5.QtWidgets import QApplication
from ui import GatePassSystem
from database import setup_database

def main():
    setup_database()
    app = QApplication(sys.argv)
    main_window = GatePassSystem()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
