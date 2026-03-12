from Fluke8588A import Fluke8588A
from main_window import MainWindow

class AppController:

	def __init__(self):
		self._view = MainWindow()
		self._view.set_disconnected()
		self._connect_signals()
		self._view.show()
		self._instr_ctrl=None

	def _connect_signals(self):
		self._view.read_requested.connect(self._on_read)
		self._view.init_requested.connect(self._on_init)

	def _on_read(self):
		if not self._instr_ctrl.is_connected:
			self._view.set_status("ERROR: not connected.")
			return
		try:
			self._meas_ctrl.read()
		except Exception as e:
			self._view.set_status(f"Read error: {e}")
	
	def _on_init(self):
		if self._instr_ctrl != None and self._instr_ctrl.is_connected():
			self._instr_ctrl.close()	
		self._instr_ctrl=Fluke8588A(self._view.current_gpib_address)
		self._view.set_connected()