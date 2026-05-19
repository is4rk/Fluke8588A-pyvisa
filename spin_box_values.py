from config import InstrumentConfig
# UI display lists — what gets shown in combo boxes and spinboxes
# These are the values the user sees and selects in the interface.
# Instrument validation lives in InstrumentConfig, not here.

FUNCTIONS = ["", "DCV", "DCI", "ACV", "ACI", "OHMS", "DIGITIZE"]

DCV_RANGE =     ["Auto", "100 mV", "1 V", "10 V", "100 V", "1 kV"]
DCV_RANGE_VAL = ["AUTO ON", 1e-1, 1, 1e1, 1e2, 1e3]

DCI_RANGE =     ["AUTO ON", "10 μA", "100 μA", "1 mA", "10 mA", "100 mA", "1 A", "10 A", "30 A"]
DCI_RANGE_VAL = ["AUTO ON", 1e-7, 1e-6, 1e-3, 1e-2, 1e-1, 1, 1e1, 3e1]

DCV_ZIN = ["Auto", "10 MΩ", "1 MΩ"]

DC_DIGIT_VAL = sorted(InstrumentConfig.VALID_RESOLUTIONS_DC_DIGITS)  # single source of truth
AC_DIGIT_VAL = sorted(InstrumentConfig.VALID_RESOLUTIONS_AC_DIGITS)

AUTO_FAST_VALUES = [1e-2, 1e-1, 1, 1e1, 1e2]  # values for autofast at 4,5,6,7,8 digits

OHM_MODES = ["2W NORMAL", "4W NORMAL", "4W Tru", "2W HV", "4W HV"]
OHM_RANGE = ["AUTO ON", "1 Ω", "10 Ω", "100 Ω", "1 kΩ", "100 kΩ", "1 MΩ", "10 MΩ", "100 MΩ", "1 GΩ"]
OHM_RANGE_VAL = ["AUTO ON", 1, 1e1, 1e2, 1e3, 1e5, 1e6, 1e7, 1e8, 1e9] 

HZ=50
MAX_TIME = 10
MIN_TIME= 0.0001 
MAX_NPLC= MAX_TIME*HZ 
MIN_NPLC = 0.01 #corresponds to 0.0002 seconds, there is a descrepency that is due to machine specs




def get_functions():
    return FUNCTIONS

def get_dcv_range():
    return DCV_RANGE

def get_dci_range():
    return DCI_RANGE

def get_dcv_zin():
    return DCV_ZIN

def get_dcv_range_val(value):
    return DCV_RANGE_VAL[DCV_RANGE.index(value)]

def get_dci_range_val(value):
    return DCI_RANGE_VAL[DCI_RANGE.index(value)]  # fixed: was using DCV_RANGE_VAL

def get_dc_digit_val():
    return DC_DIGIT_VAL

def get_ac_digit_val():
    return AC_DIGIT_VAL

def get_hz():
    return HZ

def get_max_nplc():
    return MAX_NPLC

def get_min_nplc():
    return MIN_NPLC

def get_max_time():
    return MAX_TIME

def get_min_time():
    return MIN_TIME

def get_ohm_modes():
    return OHM_MODES

def get_ohm_range():
    return OHM_RANGE

def get_ohm_range_val(value):
    return OHM_RANGE_VAL[OHM_RANGE.index(value)]