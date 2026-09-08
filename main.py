"""Punctul de intrare al aplicației HealthChecker"""
import sys
from PySide6.QtWidgets import QApplication

from src.presentation.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("HealthChecker")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()