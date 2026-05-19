from spin_box_values  import *
from config import *
class Translator:
    def __init__(self):
        """Initialize the translator with any necessary calibration data."""
        self.error_value="no_trans"
    
    def impedence_to_machine(self, value):
        """
        Convert GUI impedance value to machine value.
        
        Args:
            gui_impedance: The impedance value from the GUI
            
        Returns:
            float: The translated machine value
        """
        gui_val=InstrumentConfig.VALID_IMPEDANCES_DCV
        machine_val=[DCV_ZIN]
        mapping=dict(zip(gui_val, machine_val))
        return mapping.get(value, self.error_value)
    
    def machine_to_gui(self, machine_value):
        """
        Convert machine value back to GUI impedance value.
        
        Args:
            machine_value: The impedance value from the machine
            
        Returns:
            float: The translated GUI value
        """
        gui_impedance = machine_value / 1.0  # Placeholder conversion
        return gui_impedance