from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QWidget
import os
main_window_loc = os.path.join(os.path.dirname(__file__), "ui", "mainwindow.ui")

class MainWindow(QMainWindow):
	
	init_requested = pyqtSignal()
	mode_changed = pyqtSignal(str)
	read_requested = pyqtSignal()
	set_requested = pyqtSignal()
	measurment_setup_requested = pyqtSignal()

	def __init__(self):
		super().__init__()
		uic.loadUi(main_window_loc, self)
		self._init_visibility()
		self.set_mode_visible(self.current_mode)
		self._connect_signals()

	def _init_visibility(self):
		pass
		#make it hide mode_widgets
		
	def _connect_signals(self):
		#always visible
		self.init_button.pressed.connect(self.init_requested)
		self.mode_combo.currentTextChanged.connect(self.mode_changed)
		self.read_button.pressed.connect(self.read_requested)
		self.set_button.pressed.connect(self.set_requested)
		self.dcv_measure_setup_button.pressed.connect(self.measurment_setup_requested)

	def set_disconnected(self):
		self.init_button.setEnabled(True)
		self.read_button.setEnabled(False)
		self.mode_combo.setEnabled(False)
		self.set_button.setEnabled(False)
		#add function that hides all widgets etc

	def set_connected(self):	
		self.init_button.setEnabled(True)
		self.read_button.setEnabled(True)
		self.mode_combo.setEnabled(True)
		self.set_button.setEnabled(True)	
		#add fucntion that shows current mode widgets

	@property
	def current_gpib_address(self)->int:
		return self.gpib_addr_spin.value()

	@property
	def current_dcv_range(self)->str:
		return self.dcv_range_combo.currentText()

	@property
	def current_dcv_resolution(self)->int:
		return self.dcv_res_spin.value()

	@property
	def current_dcv_measurement_mode(self)->str:
		return self.dcv_measure_setup_button.currentText()

	@property
	def current_dcv_zin(self)->str:
		return self.dcv_zin_combo.currentText()

	@property
	def current_mode(self)->str:
		return self.mode_combo.currentText()
		
	def set_mode_visible(self, mode: str):
		self.dcv_widget.setVisible(mode == "DCV")
		# self.dci_widget.setVisible(mode == "DCI")
		# self.acv_widget.setVisible(mode == "ACV")
		# self.aci_widget.setVisible(mode == "ACI")

	def set_status(self, startus: str):
		self.status_label.setText(str)