import sys
import os
import SpinBoxValues as sbv
# Import the custom instrument class module
import Fluke8588A as Fluke
from PyQt6.QtWidgets import QApplication, QWidget, QDialog, QSpinBox, QDoubleSpinBox
# Import the module that handles runtime loading of .ui files
from PyQt6 import uic 
# Import the specific error type to catch connection issues
from Fluke8588A import pyvisa # Use the pyvisa module imported/mocked in the Fluke file
VisaIOError = pyvisa.errors.VisaIOError


# --- PyQt6 Application Logic ---
class MainWindow: 
	def __init__(self):
		# Load the UI file dynamically from the same directory as this module.
		ui_path = os.path.join(os.path.dirname(__file__), "mainwindow.ui")
		try:
			self.ui = uic.loadUi(ui_path)
		except FileNotFoundError:
			print(f"Error: The file '{ui_path}' was not found.")
			return

		# Initialize the instrument state
		self.fluke_dmm = None
		self.dcv_measure_setup_window = None

		# Helper to fetch widgets and warn when missing so user sees clear issues
		def get_widget(name, required=False):
			# Try direct attribute first (for top-level widgets)
			w = getattr(self.ui, name, None)
			# If not found, search in widget tree using findChild
			if w is None:
				from PyQt6.QtWidgets import QWidget
				w = self.ui.findChild(QWidget, name)
			if w is None:
				if required:
					print(f"REQUIRED UI widget missing: {name}")
				else:
					print(f"UI widget missing: {name}")
			return w

		# Use helper for consistent warnings
		self.initButton = get_widget('init_button', required=True)
		self.gpibSpin = get_widget('gpib_addr_spin', required=True)
		self.readButton = get_widget('read_button', required=True)
		self.statusLabel = get_widget('status_label', required=True)
		self.measureDisplay = get_widget('measure_display_label', required=True)
		self.modeCombo = get_widget('mode_combo', required=True)
		self.measureModeLabel= get_widget('measure_mode_label', required=True)
		self.plcLabel = get_widget('plc_label', required=False)
		self.timeLabel= get_widget('time_label', required=False)


		# DCV Controls
		self.dcv_range_label = get_widget('dcv_range_label', required=False)
		self.dcv_range_combo = get_widget('dcv_range_combo', required=False)
		self.dcv_res_label = get_widget('dcv_res_label', required=False)
		self.dcv_res_spin = get_widget('dcv_res_spin', required=False)
		self.dcv_zin_label = get_widget('dcv_zin_label', required=False)
		self.dcv_zin_combo = get_widget('dcv_zin_combo', required=False)
		self.dcv_label_4 = get_widget('dcv_label_4', required=False)
		self.dcv_measure_setup_button = get_widget('dcv_measure_setup_button', required=False)

		# DCI Controls
		self.dci_range_label = get_widget('dci_range_label', required=False)
		self.dci_range_combo = get_widget('dci_range_combo', required=False)
		self.dci_res_label = get_widget('dci_res_label', required=False)
		self.dci_res_spin = get_widget('dci_res_spin', required=False)
		self.dci_label_3 = get_widget('dci_label_3', required=False)
		self.dci_label_4 = get_widget('dci_label_4', required=False)
		self.dci_measure_setup_button = get_widget('dci_measure_setup_button', required=False)
		

		#Configure GPIB spin and mode
		if self.gpibSpin:
			try:
				self.gpibSpin.setRange(0, 30) # Set valid GPIB address range
				self.gpibSpin.setValue(9) # Set default GPIB address to 9
			except Exception as e:
				print(f"Error configuring 'gpib_addr_spin': {e}")
		self.mode=""
		self.measureMode=""
		self.plc=-1
		self.time=-1
		
		# Confugure labels
		if self.statusLabel:
			self.statusLabel.setText("Ready. Click 'Initialize DMM' to connect.")
		if self.measureDisplay:
			self.measureDisplay.setText("---")
		if self.measureModeLabel:
			self.measureModeLabel.setText("Mode: N/A") if self.mode == "" else self.measureModeLabel.setText(f"Mode: {self.mode}")
		if self.plcLabel:
			self.plcLabel.setText("PLC: N/A") if self.plc < 0 else self.plcLabel.setText(f"PLC: {self.plc}")
		if self.timeLabel:
			self.timeLabel.setText("Time: N/A") if self.time < 0 else self.timeLabel.setText(f"Time: {self.time} s")
		
		# Configure DCV resolution spinbox
		if self.dcv_res_spin:
			max_digits = getattr(self.fluke_dmm, 'max_digits', 8)
			min_digits = getattr(self.fluke_dmm, 'min_digits', 4)
			try:
				self.dcv_res_spin.setRange(min_digits, max_digits)
			except Exception:
				self.dcv_res_spin.setRange(4, 8)
			self.dcv_res_spin.setValue(7)
		if self.dcv_measure_setup_button:
			self.dcv_measure_setup_button.clicked.connect(self.open_dc_measure_setup)

		# Configure DCI resolution spinbox
		if self.dci_res_spin:
			max_digits = getattr(self.fluke_dmm, 'max_digits', 8)
			min_digits = getattr(self.fluke_dmm, 'min_digits', 4)
			try:
				self.dci_res_spin.setRange(min_digits, max_digits)
			except Exception:
				self.dci_res_spin.setRange(4, 8)
			self.dci_res_spin.setValue(7)
		if self.dci_measure_setup_button:
			self.dci_measure_setup_button.clicked.connect(self.open_dc_measure_setup)
		# Set initial text
		
		


		# Connect Signals 
		if self.initButton:
			self.initButton.clicked.connect(self.initialize_instrument)
		if self.readButton:
			self.readButton.clicked.connect(self.read_value)
			self.readButton.setEnabled(False) # Disable read until initialized

		# Populate combo boxes wfrom SpinBoxValues module
		if self.modeCombo is not None:
			self.modeCombo.addItems(sbv.getFunctions())
			self.modeCombo.currentTextChanged.connect(lambda text: self.set_mode(text))
			self.modeCombo.setCurrentIndex(0)
		if self.dcv_range_combo is not None:
			self.dcv_range_combo.addItems(sbv.getDcvRange())
			self.dcv_range_combo.setCurrentIndex(0)
		if self.dcv_zin_combo is not None:
			self.dcv_zin_combo.addItems(sbv.getDcvZin())
			self.dcv_zin_combo.setCurrentIndex(0)

		if self.dci_range_combo is not None:
			self.dci_range_combo.addItems(sbv.getDciRange())
			self.dci_range_combo.setCurrentIndex(0)

		
		

		# 3. Show the window
		self.ui.show()

	def initialize_instrument(self):
		"""Initializes the Fluke DMM and updates the status label."""
		if self.fluke_dmm is None:
			# determine address from widget (or fallback to 9)
			addr = None
			if self.gpibSpin:
				try:
					addr = int(self.gpibSpin.value())
				except Exception:
					addr = 9
			else:
				addr = 9
			if self.statusLabel:
				self.statusLabel.setText(f"Attempting to connect to Fluke 8588A at GPIB {addr}...")
			try:
				# Instantiate the DMM class (this connects the hardware)
				self.fluke_dmm = Fluke.Fluke8588A(addr)
				# Success feedback
				idn_string = self.fluke_dmm.identify().strip()
				if self.statusLabel:
					self.statusLabel.setText(f"SUCCESS: DMM Initialized. ID: {idn_string}")
				if self.readButton:
					self.readButton.setEnabled(True) # Enable read button
				
			except VisaIOError as e:
				error_msg = f"ERROR: Initialization Failed (VISA). Is instrument on/connected? Details: {e}"
				print(error_msg)
				if self.statusLabel:
					self.statusLabel.setText(error_msg)
				self.fluke_dmm = None 
				
			except Exception as e:
				error_msg = f"ERROR: Initialization Failed (General). Details: {e}"
				print(error_msg)
				if self.statusLabel:
					self.statusLabel.setText(error_msg)
				self.fluke_dmm = None 
				
		else:
			if self.statusLabel:
				self.statusLabel.setText("Instrument is already connected.")

	def read_value(self):
			"""Reads a single DC voltage from the DMM and updates the display label."""				
			
			if self.fluke_dmm is None:
				if self.statusLabel:
					self.statusLabel.setText("ERROR: Instrument not initialized. Click 'Initialize' first.")
				return
			if self.statusLabel:
				self.statusLabel.setText(f"Reading {self.mode}...")
			try:
				if self.measureDisplay:
					self.measureDisplay.setText(self.fluke_dmm.read())
				if self.statusLabel:
					self.statusLabel.setText("Read successfully.")
					
			except VisaIOError as e:
				error_msg = f"ERROR reading DMM: Connection lost or timeout. Details: {e}"
				print(error_msg)
				if self.statusLabel:
					self.statusLabel.setText(error_msg)
			except Exception as e:
				error_msg = f"ERROR reading DMM: General error. Details: {e}"
				print(error_msg)
				if self.statusLabel:
					self.statusLabel.setText(error_msg)
	def _update_ui_for_mode(self, mode):
		"""Show/hide control groups based on selected mode."""
		if mode == "DCV":
			# Show and enable DCV controls
			for widget in [self.dcv_range_label, self.dcv_range_combo, self.dcv_res_label, 
						   self.dcv_res_spin, self.dcv_zin_label, self.dcv_zin_combo,
						   self.dcv_label_4, self.dcv_measure_setup_button]:
				if widget:
					widget.setVisible(True)
					widget.setEnabled(True)
			
			# Hide and disable DCI controls
			for widget in [self.dci_range_label, self.dci_range_combo, self.dci_res_label,
						   self.dci_res_spin, self.dci_label_3, self.dci_label_4,
						     self.dci_measure_setup_button]:
				if widget:
					widget.setVisible(False)
					widget.setEnabled(False)
				
		elif mode == "DCI":
			# Hide and disable DCV controls
			for widget in [self.dcv_range_label, self.dcv_range_combo, self.dcv_res_label,
						   self.dcv_res_spin, self.dcv_zin_label, self.dcv_zin_combo,
						   self.dcv_label_4, self.dcv_measure_setup_button]:
				if widget:
					widget.setVisible(False)
					widget.setEnabled(False)
			
			# Show and enable DCI controls
			for widget in [self.dci_range_label, self.dci_range_combo, self.dci_res_label,
						   self.dci_res_spin, self.dci_label_3, self.dci_label_4,
						   self.dci_measure_setup_button]:
				if widget:
					widget.setVisible(True)
					widget.setEnabled(True)
		else:
			# For other modes (ACV, ACI, OHMS, DIGITIZE), hide all mode-specific controls
			for widget in [self.dcv_range_label, self.dcv_range_combo, self.dcv_res_label,
						   self.dcv_res_spin, self.dcv_zin_label, self.dcv_zin_combo,
						   self.dcv_label_4, self.dcv_measure_setup_button,
						   self.dci_range_label, self.dci_range_combo, self.dci_res_label,
						   self.dci_res_spin, self.dci_label_3, self.dci_label_4,
						   self.dci_measure_setup_button]:
				if widget:
					widget.setVisible(False)
					widget.setEnabled(False)

	def set_mode(self, mode):
		"""
		Set UI mode and (if connected) configure the instrument.
		"""
		self.mode = mode
		# Update UI labels and visibility
		self._update_ui_for_mode(mode)
		# Update status
		if self.statusLabel:
			self.statusLabel.setText(f"Mode set to {mode}. Ready to read.")

		# If instrument is already initialized, configure it
		if getattr(self, 'fluke_dmm', None) is None:
			return

		instr = self.fluke_dmm
		try:
			if mode == "DCV":
				"""
				label_1: range, has 6 possible values
				label_2: resolution, 4-8
				label_3: z in, has 3 possible values
				label_4: empty
				label_5: measure set up, opens pop up
				"""
				try:
					instr.init_dcv(
						self.fluke_dmm, 
						self.dcv_range_combo.currentText(), 
						self.dcv_res_spin.value(),  
						self.plc.value(), 
						self.measureDisplay.text(),
						self.dcv_zin_combo.currentText(), 
						)
				except TypeError:
					# different signature — try calling without args
					try:
						instr.init_dcv()
					except Exception as e:
						print(f"Failed to init DCV mode: {e}")
				else:
					print("Instrument has no DCV setter/init method; sending SCPI function command")
					instr.write(":FUNC 'VOLT:DC'")
			elif mode == "DCI":
				"""
				label_1: range, has 9 possible values
				label_2: resolution, 4-8
				label_3: empty
				label_4: empty
				label_5: measure set up, opens pop up
				"""
				if hasattr(instr, 'set_dci'):
					instr.set_dci()
				elif hasattr(instr, 'init_dci'):
					try:
						instr.init_dci()
					except Exception:
						print("init_dci exists but failed when called without args")
				else:
					# Best-effort: set current DC function via SCPI
					try:
						instr.write(":FUNC 'CURR:DC'")
					except Exception as e:
						print(f"Failed to set DCI mode via SCPI: {e}")
			else:
				print(f"Unknown mode requested: {mode}")
		except Exception as e:
			print(f"Error while configuring instrument mode {mode}: {e}")

	def open_dc_measure_setup(self):
		"""Open the DC Measure Setup dialog window."""
		ui_path = os.path.join(os.path.dirname(__file__), "measSetupDC.ui")
		try:
			if self.dcv_measure_setup_window is None:
				# Create a QDialog and load the UI into it
				self.dcv_measure_setup_window = QDialog(self.ui)
				uic.loadUi(ui_path, self.dcv_measure_setup_window)
				
				# Connect the existing buttons from Qt Designer
				buttonBox = self.dcv_measure_setup_window.findChild(QWidget, "buttonBox")
				if buttonBox:
					buttonBox.accepted.connect(self.dcv_measure_setup_window.accept)
					buttonBox.rejected.connect(self.dcv_measure_setup_window.reject)
			
			# Use exec() to block until dialog closes
			result = self.dcv_measure_setup_window.exec()
			
			# After dialog closes, capture values
			if result == 1:  # 1 = Accepted/OK, 0 = Rejected/Cancel
				# Retrieve widget values from measSetupDC.ui
				self.plc = self.dcv_measure_setup_window.plc_spin.value()
				self.time = self.dcv_measure_setup_window.time_spin.value()
				
				if self.fluke_dmm:
					actualPlc = self.fluke_dmm.set_plc(self.plc)
					if self.plcLabel:
						self.plcLabel.setText(f"PLC: {actualPlc}")
					if self.timeLabel:
						self.timeLabel.setText(f"Time: {self.time} s")
					print(f"Settings saved: PLC={self.plc}, Time={self.time}")
				else:
					print("Instrument not initialized. Settings stored but not applied to device.")
			
		except FileNotFoundError:
			print(f"Error: The file '{ui_path}' was not found.")
		
# --- Application Entry Point ---
if __name__ == "__main__":
	app = QApplication(sys.argv)
	
	main_window_instance = MainWindow()
	
	if hasattr(main_window_instance, 'ui'):
		sys.exit(app.exec())