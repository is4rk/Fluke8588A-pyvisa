from Fluke8588A import Fluke8588A
from main_window import MainWindow

class AppController:

	def __init__(self):
		self._view = MainWindow()
		self._view.set_disconnected()
		self._connect_signals()
		self._view.show()

	def _connect_signals(self):
		self._view.read_requested.connect(self._on_read)
		self._view.init_requested.connect(self._on_init)
		self._view.mode_changed.connect(self._on_mode_change)
	
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
