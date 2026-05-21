from instrument_controller import InstrumentController as InstrumentController 
from main_window import MainWindow
from dc_measurment_setup import DcMeasurmentWindow
from trigger_setup import TriggerWindow
from settings import DcvSettings, DciSettings, OhmsSettings
from measurment_controller import ReadingThread
from translator import Translator

class AppController:
	TEST_MODE = True  # Set to False to disable debug output

	def __init__(self):
		self._view = MainWindow()
		self._meas_pop_up = DcMeasurmentWindow()
		# self._trigger_pop_up = TriggerWindow()
		self._view.set_disconnected()
		
		# Initialize settings objects with default values
		self._dcv_settings = DcvSettings(
			range_mode="AUTO",
			range_val="AUTO ON",
			resolution=4,
			zin="AUTO",
			aperture_mode="AUTO",
			time=0.1
		)
		self._dci_settings = DciSettings(
			range_mode="AUTO",
			range_val="AUTO ON",
			resolution=4,
			aperture_mode="AUTO",
			time=0.1
		)
		self._ohms_settings = OhmsSettings(
			four=False, #four wire or 2 wire
			range_val="AUTO ON",
			resolution=4,
			mode="2W NORMAL",
			filter=False,
			low_i=False,
			aperture_mode="AUTO",
			time=0.1
		)
		
		self._connect_signals()
		self._view.show()
		self._instr_ctrl=InstrumentController()
		self._reading_thread= None
		self._translator = Translator()

	def _connect_signals(self):
		self._view.init_requested.connect(self._on_init)
		self._view.mode_changed.connect(self._on_mode_change)
		self._view.read_requested.connect(self._on_read)
		self._view.set_requested.connect(self._on_set)
		self._view.measurment_setup_requested.connect(self._on_measurment_setup_press)
		self._view.dcv_signal.connect(self._on_dcv_setting_change)
		self._view.dci_signal.connect(self._on_dci_setting_change)
		self._view.ohms_signal.connect(self._on_ohms_setting_change)
		self._meas_pop_up.mode_select.connect(self._on_aperture_mode_changed)
		self._meas_pop_up.time_select.connect(self._on_time_changed)
		self._meas_pop_up.nplc_select.connect(self._on_nplc_changed)
		self._view.continuous_start_requested.connect(self._on_continuous_start)
		self._view.continuous_stop_requested.connect(self._on_continuous_stop)

	def _on_read(self):
		if self.TEST_MODE: print(f">>> _on_read")
		if not self._instr_ctrl.is_connected():
			self._view.set_status("ERROR: not connected.")
			if self.TEST_MODE: print(f"<<< _on_read (not connected)")
			return
		try:
			value=self._instr_ctrl.read()
			print(value) # REMOVE
			self._view.set_read(value)
			if self.TEST_MODE: print(f"<<< _on_read (value={value})")
		except Exception as e:
			self._view.set_status(f"Read error: {e}")
			if self.TEST_MODE: print(f"<<< _on_read (error={e})")	
	
	def _on_init(self):
		if self.TEST_MODE: print(f">>> _on_init (gpib_address={self._view.current_gpib_address})")
		if hasattr(self, '_instr_ctrl'):
			if self._instr_ctrl.is_connected():
				self._instr_ctrl.disconnect()
		self._instr_ctrl.connect(self._view.current_gpib_address)
		self._view.set_connected()
		self._view.set_status("Connected")
		if self.TEST_MODE: print(f"<<< _on_init")
	
	def _on_mode_change(self):
		if self.TEST_MODE: print(f">>> _on_mode_change (mode={self._view.current_mode})")
		self._view.set_mode_visible(self._view.current_mode)
		if self.TEST_MODE: print(f"<<< _on_mode_change")

	def _on_set(self):
		mode=self._view.current_mode
		if self.TEST_MODE: print(f">>> _on_set (mode={mode})")
		new_settings=self.get_settings_from_mode(mode)
		actual_settings=self._instr_ctrl.set(mode, new_settings)
		
		#Update internal settings with what the instrument actually accepted
		if mode == "DCV":
			self._dcv_settings = actual_settings
		elif mode == "DCI":
			self._dci_settings = actual_settings
		elif mode == "OHMS":
			self._ohms_settings = actual_settings
		
		# Update the GUI to reflect actual settings
		self._view.set_status(f"{mode} settings applied")
		self._refresh_ui_settings()
		if self.TEST_MODE: print(f"<<< _on_set")

	def get_settings_from_mode(self, mode: str):
		if mode == "DCV":
			return self._dcv_settings
		if mode == "DCI":
			return self._dci_settings
		if mode == "OHMS":
			return self._ohms_settings
	
	def _refresh_ui_settings(self):
		"""Update UI to show current settings from app controller"""
		mode = self._view.current_mode
		if mode == "DCV":
			self._view.dcv_signal.emit(self._dcv_settings)
		elif mode == "DCI":
			self._view.dci_signal.emit(self._dci_settings)
		elif mode == "OHMS":
			self._view.ohms_signal.emit(self._ohms_settings)

	def _on_measurment_setup_press(self):
		self._meas_pop_up.show()

	def _on_trigger_press(self):
		self._trigger_pop_up.show()
	def _on_aperture_mode_changed(self, mode):
		if self.TEST_MODE: print(f">>> _on_aperture_mode_changed (mode={mode})")
		self._current_aperture_mode = mode
		self._view.set_aperture_mode(mode)
		current_mode = self._view.current_mode
		if current_mode == "DCV":
			self._dcv_settings.aperture_mode = mode
			self._on_dcv_setting_change(self._dcv_settings)
		elif current_mode == "DCI":
			self._dci_settings.aperture_mode = mode
			self._on_dci_setting_change(self._dci_settings)
		elif current_mode == "OHMS":
			self._ohms_settings.aperture_mode = mode
			self._on_ohms_setting_change(self._ohms_settings)
		if self.TEST_MODE: print(f"<<< _on_aperture_mode_changed")

	def _on_time_changed(self, time):
		if self.TEST_MODE: print(f">>> _on_time_changed (time={time})")
		self._current_time = time
		self._view.set_time_value(time)
		current_mode = self._view.current_mode
		if current_mode == "DCV":
			self._dcv_settings.time = time
			self._on_dcv_setting_change(self._dcv_settings)
		elif current_mode == "DCI":
			self._dci_settings.time = time
			self._on_dci_setting_change(self._dci_settings)
		elif current_mode == "OHMS":
			self._ohms_settings.time = time
			self._on_ohms_setting_change(self._ohms_settings)
		if self.TEST_MODE: print(f"<<< _on_time_changed")

	def _on_nplc_changed(self, nplc):
		if self.TEST_MODE: print(f">>> _on_nplc_changed (nplc={nplc})")
		self._current_nplc = nplc
		self._view.set_nplc_value(nplc)
		current_mode = self._view.current_mode
		if current_mode == "DCV":
			self._dcv_settings.resolution = nplc
			self._on_dcv_setting_change(self._dcv_settings)
		elif current_mode == "DCI":
			self._dci_settings.resolution = nplc
			self._on_dci_setting_change(self._dci_settings)
		elif current_mode == "OHMS":
			self._ohms_settings.resolution = nplc
			self._on_ohms_setting_change(self._ohms_settings)
		if self.TEST_MODE: print(f"<<< _on_nplc_changed")

	def _set_ui_aperture_settings(self):
		self._view.set_aperture_mode()
		self._view.set_time_value()
		
	
	def _on_dcv_setting_change(self, settings: DcvSettings):
		if self.TEST_MODE: print(f">>> _on_dcv_setting_change (range_val={settings.range_val}, resolution={settings.resolution}, zin={settings.zin})")
		translated_settings = DcvSettings(
			range_mode=settings.range_mode,
			range_val=self._translator.gui_to_machine(settings.range_val),
			resolution=settings.resolution,
			zin=self._translator.gui_to_machine(settings.zin),
			aperture_mode=settings.aperture_mode,
			time=settings.time
		)
		print(translated_settings.zin)
		self._dcv_settings = translated_settings
		if self.TEST_MODE: print(f"<<< _on_dcv_setting_change")

	
	def	_on_dci_setting_change(self, settings: DciSettings):
		if self.TEST_MODE: print(f">>> _on_dci_setting_change (range_val={settings.range_val}, resolution={settings.resolution})")
		translated_settings = DciSettings(
			range_mode=settings.range_mode,
			range_val=self._translator.gui_to_machine(settings.range_val),
			resolution=settings.resolution,
			aperture_mode=settings.aperture_mode,
			time=settings.time
		)
		self._dci_settings = translated_settings
		if self.TEST_MODE: print(f"<<< _on_dci_setting_change")

	def _on_ohms_setting_change(self, settings: OhmsSettings):
		if self.TEST_MODE: print(f">>> _on_ohms_setting_change (range_val={settings.range_val}, mode={settings.mode}, resolution={settings.resolution})")
		translated_settings = OhmsSettings(
			four=settings.four,
			range_val=self._translator.gui_to_machine(settings.range_val),
			resolution=settings.resolution,
			mode=settings.mode,
			filter=settings.filter,
			low_i=settings.low_i,
			aperture_mode=settings.aperture_mode,
			time=settings.time
		)
		self._ohms_settings = translated_settings
		if settings.mode.startswith("4W"):
			self._ohms_settings.four=True
		elif settings.mode.startswith("2W"):
			self._ohms_settings.four=False
		if self.TEST_MODE: print(f"<<< _on_ohms_setting_change")

	def _on_continuous_start(self):
		if self.TEST_MODE: print(f">>> _on_continuous_start")
		if self._reading_thread is not None:
			if self.TEST_MODE: print(f"<<< _on_continuous_start (thread already running)")
			return
		self._reading_thread=ReadingThread(self._instr_ctrl)
		self._reading_thread.reading_ready.connect(self._view.set_read) #emits from measurment_controller are redirected to view
		self._reading_thread.start()
		self._view.start_button.setEnabled(False)
		self._view.stop_button.setEnabled(True)
		self._view.set_status("Continuous reading started.")
		if self.TEST_MODE: print(f"<<< _on_continuous_start")
		

	def _on_continuous_stop(self):
		if self.TEST_MODE: print(f">>> _on_continuous_stop")
		if self._reading_thread is None:
			if self.TEST_MODE: print(f"<<< _on_continuous_stop (no thread running)")
			return True
		self._reading_thread.stop()
		self._reading_thread = None
		self._view.set_status("Stopped.")
		self._view.stop_button.setEnabled(False)
		self._view.start_button.setEnabled(True)
		if self.TEST_MODE: print(f"<<< _on_continuous_stop")
