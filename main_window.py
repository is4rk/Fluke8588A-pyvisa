from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow
from spin_box_values import (
    get_functions, get_dcv_range, get_dci_range,
    get_dcv_zin, get_dc_digit_val
)
from config import InstrumentConfig
import os

UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "mainwindow.ui")
#
# Buttons:    init_button, read_button, set_button
#             dcv_measure_setup_button, dci_measure_setup_button
# SpinBoxes:  gpib_addr_spin (QSpinBox)
#             dcv_res_spin (QSpinBox), dci_res_spin (QSpinBox)
# ComboBoxes: mode_combo, dcv_range_combo, dcv_zin_combo, dci_range_combo
# Labels:     status_label, measure_display_label, measure_mode_label
#             nplc_label, time_label
#             dcv_range_label, dcv_res_label, dcv_zin_label, dcv_label_4
#             dci_range_label, dci_res_label, dci_label_3, dci_label_4

# Mode widget groups — used by set_mode_visible() to show/hide controls
MODE_WIDGETS = {
    "DCV": [
        "dcv_range_label", "dcv_range_combo",
        "dcv_res_label",   "dcv_res_spin",
        "dcv_zin_label",   "dcv_zin_combo",
        "dcv_label_4",     "dcv_measure_setup_button",
    ],
    "DCI": [
        "dci_range_label", "dci_range_combo",
        "dci_res_label",   "dci_res_spin",
        "dci_label_3",     "dci_label_4",
        "dci_measure_setup_button",
    ],
}

ALL_MODE_WIDGETS = [w for widgets in MODE_WIDGETS.values() for w in widgets]


class MainWindow(QMainWindow):
    """
    Pure view. Loads mainwindow.ui, exposes widgets as properties,
    emits signals on user actions. Contains zero business logic.
    """

    # ── Signals ───────────────────────────────────────────────────────────────
    # Emitted when the user clicks Initialize with the chosen GPIB address
    init_requested = pyqtSignal(int)
    # Emitted when the user clicks Read
    read_requested = pyqtSignal()
    # Emitted when the user clicks Set
    set_requested = pyqtSignal()
    # Emitted when the user changes the mode combo
    mode_selected = pyqtSignal(str)
    # Emitted when the user clicks the DCV or DCI measure setup button
    setup_requested = pyqtSignal(str)   # str = current mode e.g. "DCV"

    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self._init_widgets()
        self._connect_internal_signals()

    # ── Internal setup ────────────────────────────────────────────────────────

    def _init_widgets(self):
        """Populate combo boxes and set initial widget states."""
        # Mode combo
        self.mode_combo.addItems(get_functions())

        # DCV controls
        self.dcv_range_combo.addItems(get_dcv_range())
        self.dcv_zin_combo.addItems(get_dcv_zin())
        self.dcv_res_spin.setRange(
            min(get_dc_digit_val()),
            max(get_dc_digit_val())
        )
        self.dcv_res_spin.setValue(InstrumentConfig.DEFAULT_RESOLUTION)

        # DCI controls
        self.dci_range_combo.addItems(get_dci_range())
        self.dci_res_spin.setRange(
            min(get_dc_digit_val()),
            max(get_dc_digit_val())
        )
        self.dci_res_spin.setValue(InstrumentConfig.DEFAULT_RESOLUTION)

        # GPIB spinbox
        self.gpib_addr_spin.setRange(0, 30)
        self.gpib_addr_spin.setValue(InstrumentConfig.DEFAULT_ADDRESS)

        # Initial UI state
        self.read_button.setEnabled(False)
        self.set_button.setEnabled(False)
        self.set_status("Ready. Click 'Initialize' to connect.")
        self.set_reading("---")
        self.set_mode_visible(self.mode_combo.currentText())

    def _connect_internal_signals(self):
        """Connect widget signals to this class's outgoing signals."""
        self.init_button.clicked.connect(
            lambda: self.init_requested.emit(self.gpib_addr_spin.value())
        )
        self.read_button.clicked.connect(self.read_requested)
        self.set_button.clicked.connect(self.set_requested)
        self.mode_combo.currentTextChanged.connect(self.mode_selected)
        self.mode_combo.currentTextChanged.connect(self.set_mode_visible)
        self.dcv_measure_setup_button.clicked.connect(
            lambda: self.setup_requested.emit("DCV")
        )
        self.dci_measure_setup_button.clicked.connect(
            lambda: self.setup_requested.emit("DCI")
        )

    # ── Public slots — called by AppController ─────────────────────────────

    def set_status(self, message: str):
        """Update the status bar label at the bottom of the window."""
        self.status_label.setText(message)

    def set_reading(self, value: str):
        """Update the measurement display label."""
        self.measure_display_label.setText(value)

    def set_mode_label(self, mode: str):
        """Update the mode info label."""
        self.measure_mode_label.setText(f"Mode: {mode}")

    def set_nplc_label(self, nplc: float):
        """Update the NPLC info label."""
        self.nplc_label.setText(f"NPLC: {nplc}")

    def set_time_label(self, time: float):
        """Update the time info label."""
        self.time_label.setText(f"Time: {time} s")

    def set_connected(self, connected: bool):
        """Enable or disable controls based on connection state."""
        self.read_button.setEnabled(connected)
        self.set_button.setEnabled(connected)
        self.init_button.setEnabled(not connected)

    def set_mode_visible(self, mode: str):
        """Show controls for the active mode, hide all others."""
        active_widgets = MODE_WIDGETS.get(mode, [])
        for widget_name in ALL_MODE_WIDGETS:
            widget = getattr(self, widget_name, None)
            if widget:
                visible = widget_name in active_widgets
                widget.setVisible(visible)
                widget.setEnabled(visible)


# ── Standalone test ───────────────────────────────────────────────────────────
# Run this file directly to visually check the UI loads correctly,
# before wiring it to any controllers.
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
