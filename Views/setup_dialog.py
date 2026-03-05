import os
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QWidget
from ..Config_Data.config import InstrumentConfig

UI_PATH = os.path.join(os.path.dirname(__file__), "ui", "measSetupDC.ui")

# Widget names from measSetupDC.ui:
#
# QCheckBox:      checkBox_1 (Auto), checkBox_2 (Auto fast), checkBox_3 (Manual)
#                 — all in buttonGroup (mutually exclusive)
# QDoubleSpinBox: nplc_spin, time_spin
# QLabel:         plc_label, time_label
# QDialogButtonBox: buttonBox (OK / Cancel)


class SetupDialog(QDialog):
    """
    Thin wrapper around measSetupDC.ui.

    Usage:
        dialog = SetupDialog(parent)
        if dialog.exec():
            nplc = dialog.nplc
            time = dialog.time
            mode = dialog.measure_mode
    """

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        uic.loadUi(UI_PATH, self)
        self._init_widgets()
        self._connect_buttons()

    # ── Internal setup ────────────────────────────────────────────────────────

    def _init_widgets(self):
        """Set sensible defaults on the spinboxes."""
        self.nplc_spin.setRange(InstrumentConfig.NPLC_MIN, InstrumentConfig.NPLC_MAX)
        self.nplc_spin.setValue(1.0)
        self.nplc_spin.setDecimals(3)

        # Time spinbox range in seconds (0.001 NPLC at 50Hz = 20μs)
        self.time_spin.setRange(0.00002, 10.0)
        self.time_spin.setValue(0.02)
        self.time_spin.setDecimals(5)

        # Default mode selection
        self.checkBox_1.setChecked(True)  # Auto

    def _connect_buttons(self):
        """Wire the OK/Cancel buttonBox to accept/reject."""
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    # ── Read-only properties — available after exec() returns True ────────────

    @property
    def nplc(self) -> float:
        """NPLC value chosen by the user."""
        return self.nplc_spin.value()

    @property
    def time(self) -> float:
        """Integration time in seconds chosen by the user."""
        return self.time_spin.value()

    @property
    def measure_mode(self) -> str:
        """
        Aperture mode chosen by the user.
        Returns "Auto", "Auto fast", or "Manual".
        """
        if self.checkBox_1.isChecked():
            return "Auto"
        elif self.checkBox_2.isChecked():
            return "Auto fast"
        elif self.checkBox_3.isChecked():
            return "Manual"
        return ""

    def set_values(self, nplc: float, time: float, mode: str):
        """
        Pre-populate the dialog with existing values before opening.
        Call this before exec() to restore previous settings.
        """
        self.nplc_spin.setValue(nplc)
        self.time_spin.setValue(time)
        self.checkBox_1.setChecked(mode == "Auto")
        self.checkBox_2.setChecked(mode == "Auto fast")
        self.checkBox_3.setChecked(mode == "Manual")


# ── Standalone test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dlg = SetupDialog()
    if dlg.exec():
        print(f"nplc={dlg.nplc}, time={dlg.time}, mode={dlg.measure_mode}")
    sys.exit(0)
