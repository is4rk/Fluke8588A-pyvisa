from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow
import os
dc_measurment_setup_loc = os.path.join(os.path.dirname(__file__), "ui", "dc_measurment_setup.ui")

class DcMeasurmentWindow():
	mode_select=pyqtSignal(str)

	def __init__(self):
		super().__init__()
		uic.loadUi(dc_measurment_setup_loc, self)

	def _connect_signals(self):
		pass