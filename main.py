from PyQt6.QtWidgets import QApplication
from app_controller import AppController
import sys

app = QApplication(sys.argv)
app_controller = AppController()
app.exec()