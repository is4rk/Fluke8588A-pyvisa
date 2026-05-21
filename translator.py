from spin_box_values import *
from config import InstrumentConfig as _inst_conf
class Translator:
    def __init__(self):
        """Initialize the translator with mapping dictionaries keyed by parameter type."""
        self.error_value = "NO_TRANS"
        
        # GUI → Machine mappings by parameter type
        self._gui_to_machine_maps = {
            "impedence": dict(zip(DCV_IMPEDENCE, _inst_conf.IMPEDANCES_DCV_VAL)),
            "dcv_range": dict(zip(DCV_RANGE, _inst_conf.DCV_RANGE_VAL)),
            "dci_range": dict(zip(DCI_RANGE, _inst_conf.DCI_RANGE_VAL)),
            "ohm_range": dict(zip(OHM_RANGE, _inst_conf.OHM_RANGE_VAL)),
            "ohm_mode" : dict(zip(OHM_MODES, _inst_conf.OHM_MODES_VAL))
        }
        
        # Machine → GUI mappings by parameter type (reversed)
        self._machine_to_gui_maps = {
            key: {v: k for k, v in gui_map.items()}
            for key, gui_map in self._gui_to_machine_maps.items()
        }
    
    def translate(self, param_type, gui_value):
        """
        Convert GUI value to machine value based on parameter type.
        
        Args:
            param_type: Type of parameter ("zin", "dcv_range", "dci_range", "ohm_range")
            gui_value: The GUI value to translate
            
        Returns:
            str: The machine value, or error_value if not found
        """
        mapping = self._gui_to_machine_maps.get(param_type, {})
        return mapping.get(gui_value, self.error_value)
    
    def translate_reverse(self, param_type, machine_value):
        """
        Convert machine value back to GUI value based on parameter type.
        
        Args:
            param_type: Type of parameter ("zin", "dcv_range", "dci_range", "ohm_range")
            machine_value: The machine value to translate
            
        Returns:
            str: The GUI value, or error_value if not found
        """
        mapping = self._machine_to_gui_maps.get(param_type, {})
        return mapping.get(machine_value, self.error_value)