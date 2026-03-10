from Fluke8588A import Fluke8588A
from main_window import MainWindow

class AppController:

	def __init__(self):
		self._view = MainWindow()
		self._instr_ctrl = Fluke8588A(9) #for now hard coded, should be called after set_init 
		self._connect_signals()
		self._view.show()

	def _connect_signals(self):
		self._view.read_requested.connect(self._on_read)

	def _on_read(self):
		if not self._instr_ctrl.is_connected():
			self._view.set_status("ERROR: not connected.")
			return
		try:
			self._meas_ctrl.read()
		except Exception as e:
			self._view.set_status(f"Read error: {e}")

