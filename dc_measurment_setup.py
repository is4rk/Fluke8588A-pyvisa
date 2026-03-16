from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from spin_box_values import get_min_time, get_max_time, get_min_nplc, get_max_nplc
from PyQt6.QtWidgets import QWidget
import os
dc_measurment_setup_loc = os.path.join(os.path.dirname(__file__), "ui", "dc_measurment_setup.ui")

class DcMeasurmentWindow(QWidget):
	mode_select=pyqtSignal(str)

	def __init__(self):
		super().__init__()
		uic.loadUi(dc_measurment_setup_loc, self)
		self._init_widgets()
		self._connect_time_and_nplc()


	def _init_widgets(self):
		self.nplc_spin.setRange(get_min_nplc(), get_max_nplc())
		self.time_spin.setRange(get_min_time(), get_max_time())
		self.nplc_spin.valueChanged.connect(self._update_time)

	def _update_time(self):
		self.time_spin.setValue(float(self.nplc_spin.currentValue())/50)
	
	def _update_nplc(self):

	def _connect_signals(self):
		pass