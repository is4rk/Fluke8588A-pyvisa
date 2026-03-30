from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow
import os
from spin_box_values import get_functions, get_dcv_range, get_dci_range, get_dcv_zin, get_dc_digit_val
from config import InstrumentConfig
from settings import DcvSettings, DciSettings
from plot_widget import DmmPlotWidget
main_window_loc = os.path.join(os.path.dirname(__file__), "ui", "mainwindow.ui")

class MainWindow(QMainWindow):
	
	init_requested = pyqtSignal()
	mode_changed = pyqtSignal()
	read_requested = pyqtSignal()
	set_requested = pyqtSignal()
	measurment_setup_requested = pyqtSignal()
	dcv_signal = pyqtSignal(DcvSettings)
	dci_signal = pyqtSignal(DciSettings)
	continuous_start_requested = pyqtSignal()
	continuous_stop_requested  = pyqtSignal()
	append_value = pyqtSignal(float)	

	def __init__(self):
		super().__init__()
		uic.loadUi(main_window_loc, self)
		self.set_mode_visible(self.current_mode)
		self._connect_signals()
		self._init_widgets()
		
		#TO BE MOVED TO OWN MODULE
		self.seconds:float=0.0
		self.data =[]
		self.time=[]
		
	def _connect_signals(self):
		#always visible
		self.init_button.pressed.connect(self.init_requested)
		self.mode_combo.currentTextChanged.connect(self.mode_changed)
		self.set_button.pressed.connect(self.set_requested) #to be 
		#dcv signals
		self.dcv_range_combo.currentTextChanged.connect(self._on_dcv_changed)
		self.dcv_res_spin.valueChanged.connect(self._on_dcv_changed)
		self.dcv_zin_combo.currentTextChanged.connect(self._on_dcv_changed)
		self.dcv_measure_setup_button.pressed.connect(self.measurment_setup_requested) #to be
		#dci signals
		self.dci_range_combo.currentTextChanged.connect(self._on_dci_changed)
		self.dci_res_spin.valueChanged.connect(self._on_dci_changed)
		self.dci_measure_setup_button.pressed.connect(self.measurment_setup_requested) #to be
		#reading 
		self.read_button.pressed.connect(self.read_requested)
		self.start_button.pressed.connect(self.continuous_start_requested)
		self.stop_button.pressed.connect(self.continuous_stop_requested)

	def _init_widgets(self):
		self.gpib_addr_spin.setRange(0, 30)
		self.gpib_addr_spin.setValue(InstrumentConfig.DEFAULT_ADDRESS)
		self.mode_combo.addItems(get_functions())
		#dcv
		self.dcv_range_combo.addItems(get_dcv_range())
		self.dcv_zin_combo.addItems(get_dcv_zin())
		self.dcv_res_spin.setRange(min(get_dc_digit_val()), max(get_dc_digit_val()))
		#dci
		self.dci_range_combo.addItems(get_dci_range())
		self.dci_res_spin.setRange(min(get_dc_digit_val()), max(get_dc_digit_val()))
		
		#reading
		self.stop_button.setEnabled(False)
		self.start_button.setEnabled(False)
		#plotting - connect signal to plot widget
		self.plot_widget._connect_signals(self)

	@property
	def current_gpib_address(self)->int:
		return self.gpib_addr_spin.value()

	@property
	def current_mode(self)->str:
		return self.mode_combo.currentText()


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
	def current_time(self)->float:
		return float(self.dcv_time_label.currentText())
	
	@property
	def current_nplc(self)->float:
		return float(self.dcv_nplc_label.currentText())
	


	def set_disconnected(self):
		self.init_button.setEnabled(True)
		self.read_button.setEnabled(False)
		self.mode_combo.setEnabled(False)
		self.set_button.setEnabled(False)
		self.start_button.setEnabled(False)	
		self.stop_button.setEnabled(False)

		#add function that hides all widgets etc

	def set_connected(self):	
		self.init_button.setEnabled(True)
		self.read_button.setEnabled(True)
		self.mode_combo.setEnabled(True)
		self.set_button.setEnabled(True)
		self.start_button.setEnabled(True)	
		self.stop_button.setEnabled(False)
		#add fucntion that shows current mode widgets

	def set_read(self, value: int):
		self.measure_display_label.setText(str(value))
		self.seconds+=0.1 #to be changed, by using import time
		self.time.append(self.seconds)
		self.data.append(value)
		self.append_value.emit(float(value))
		# plotData()
	
	def set_mode_visible(self, mode: str):
		self.dcv_widget.setVisible(mode == "DCV")
		self.dci_widget.setVisible(mode=="DCI")
		# self.dci_widget.setVisible(mode == "DCI")
		# self.acv_widget.setVisible(mode == "ACV")
		# self.aci_widget.setVisible(mode == "ACI")

	def set_status(self, status: str):
		self.status_label.setText(status)

	def set_aperture_mode(self, mode: str):
		self.dcv_measure_setup_button.setText(mode)

	def set_time_value(self, time: float):
		self.dcv_time_label.setText(str(time))

	def set_nplc_value(self, nplc: float):
		self.dcv_nplc_label.setText(str(nplc))

	def _on_dcv_changed(self):
		self.dcv_signal.emit(DcvSettings(
			range_mode = "AUTO" if self.dcv_range_combo.currentText() == "AUTO" else "MAN",
			range_val = self.dcv_range_combo.currentText(),
			resolution = self.dcv_res_spin.value(),
			zin = self.dcv_zin_combo.currentText(),
			aperture_mode= self.dcv_measure_setup_button.text(),
			time = self.dcv_time_label.text()
    		)
		)
		
	def _on_dci_changed(self):
		self.dci_signal.emit(DciSettings(
			range_mode = "AUTO" if self.dci_range_combo.currentText() == "AUTO" else "MAN",
			range_val = self.dci_range_combo.currentText(),
			resolution = self.dci_res_spin.value(),
			aperture_mode = self.dci_measure_setup_button.text(),
			time = self.dci_time_label.text()
		)
	)