from instrument_controller_test import InstrumentControllerTest as InstrumentController 
from main_window import MainWindow
from dc_measurment_setup import DcMeasurmentWindow
from settings import DcvSettings

class AppController:

	def __init__(self):
		self._view = MainWindow()
		self._pop_up = DcMeasurmentWindow()
		self._view.set_disconnected()
		self._connect_signals()
		self._view.show()
		self._instr_ctrl=InstrumentController()
		# Initialize popup signal values
		self._current_aperture_mode = "AUTO"
		self._current_time = 0.01
		self._current_nplc = 10.0
		# Initialize settings from current widget values
		self._on_dcv_setting_change()

	def _connect_signals(self):
		self._view.init_requested.connect(self._on_init)
		self._view.mode_changed.connect(self._on_mode_change)
		self._view.read_requested.connect(self._on_read)
		self._view.set_requested.connect(self._on_set)
		self._view.measurment_setup_requested.connect(self._on_measurment_setup_press)
		self._view.dcv_signal.connect(self._on_dcv_setting_change)
		# Connect popup signals
		self._pop_up.mode_select.connect(self._on_aperture_mode_changed)
		self._pop_up.time_select.connect(self._on_time_changed)
		self._pop_up.nplc_select.connect(self._on_nplc_changed)
	
	def _on_read(self):
		if not self._instr_ctrl.is_connected():
			self._view.set_status("ERROR: not connected.")
			return
		try:
			value=self._instr_ctrl.read()
			print(value) # REMOVE
			self._view.set_read(value)
		except Exception as e:
			self._view.set_status(f"Read error: {e}")	
	
	def _on_init(self):
		if hasattr(self, '_instr_ctrl'):
			if self._instr_ctrl.is_connected():
				self._instr_ctrl.disconnect()
		self._instr_ctrl.connect(self._view.current_gpib_address)
		self._view.set_connected()
		self._view.set_status("Connected")
	
	def _on_mode_change(self):
		self._view.set_mode_visible(self._view.current_mode)

	def _on_set(self):
		mode=self._view.current_mode
		new_settings=self.get_settings_from_mode(mode)
		self._instr_ctrl.set(mode, new_settings)

	def get_settings_from_mode(self, mode: str):
		if mode == "DCV":
			return self._dcv_settings
		# elif mode == "DCI":
		# 	return self._dci_settings

	def _on_measurment_setup_press(self):
		self._pop_up.show()

	def _on_aperture_mode_changed(self, mode):
		self._current_aperture_mode = mode
		self._view.set_aperture_mode(mode)
		self._on_dcv_setting_change()

	def _on_time_changed(self, time):
		self._current_time = time
		self._view.set_time_value(time)
		self._on_dcv_setting_change()

	def _on_nplc_changed(self, nplc):
		self._current_nplc = nplc
		self._view.set_nplc_value(nplc)
		self._on_dcv_setting_change()

	def _set_ui_aperture_settings(self):
		self._view.set_aperture_mode()
		self._view.set_time_value()\
		
	
	def _on_dcv_setting_change(self):
		self._dcv_settings = DcvSettings(
			range_mode = "AUTO" if self._view.current_dcv_range == "AUTO" else "MAN",
			range_val  = self._view.current_dcv_range,
			resolution = self._view.current_dcv_resolution,
			zin        = self._view.current_dcv_zin,
			aperture_mode = self._current_aperture_mode,
			time       = self._current_time, 
		)