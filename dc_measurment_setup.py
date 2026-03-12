from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow
import os
main_window_loc = os.path.join(os.path.dirname(__file__), "ui", "dc_measurment_setup.ui")

class DcMeasurmentWindow(QMainWindow):
	mode_select=pyqtSignal(str)

	def __init__(self):
		super().__init__()
		uic.loadUi(main_window_loc, self)
		self._init_always_visible()
		self._init_mode_widgets()
		self._connect_signals()

	def _connect_signals(self):
		#always visible
		self.init_button.pressed.connect(self.on_init_press)
		self.mode_combo.currentTextChanged.connect(self.on_mode_change)
		self.read_button.pressed.connect(self.on_read_press)
		self.set_button.pressed.connect(self.on_set_press)

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

	def _connect_slots(self):
		pass
		
	def set_mode_visible(self, mode: str):
		self.dcv_widget.setVisible(mode == "DCV")
		self.dci_widget.setVisible(mode == "DCI")
		self.acv_widget.setVisible(mode == "ACV")
		self.aci_widget.setVisible(mode == "ACI")
