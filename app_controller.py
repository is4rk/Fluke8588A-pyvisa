from Fluke8588A import Fluke8588A
from main_window import MainWindow
from dataclasses import dataclass, field

@dataclass
class DcvSettings:
	range:  str = ""
	resolution: int = 7
	input_z: str   = "AUTO"
	nplc: float = 1.0


class AppController:

	def __init__(self):
		self._view = MainWindow()
		self._view.set_disconnected()
		self._connect_signals()
		self._view.show()
		self._dcv_settings = DcvSettings()

	def _connect_signals(self):
		self._view.read_requested.connect(self._on_read)
		self._view.init_requested.connect(self._on_init)
		self._view.mode_changed.connect(self._on_mode_change)
		#mode signals
		self._view.dcv_signal.connect(self._on_dcv_setting_change)
	
	def _on_read(self):
		if not self._instr_ctrl.is_connected:
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
			if self._instr_ctrl.is_connected:
				self._instr_ctrl.close()
		self._instr_ctrl=Fluke8588A(self._view.current_gpib_address)
		self._view.set_connected()
		self._view.set_status("Connected")
	
	def _on_mode_change(self):
		self._view.set_mode_visible(self._view.current_mode)

	def _on_set(self):
		mode=self._view.current_mode
		new_settings=self.get_settings_from_mode(mode)
		pass

	def get_settings_from_mode(self, mode: str):
		if mode == "DCV":
			return self._dcv_settings
		elif mode == "DCI":
			return self._dci_settings


	def _on_dcv_setting_change(self):
		self._dcv_settings = DcvSettings(
			range_val  = self._view.current_dcv_range,
			resolution = self._view.current_dcv_resolution,
			zin        = self._view.current_dcv_zin,
			nplc       = self._view.current_nplc,
		)
