functions=["DCV", "DCI", "ACV", "ACI", "OHMS", "DIGITIZE"]
dcv_range=["Auto", "100 mV", "1 V", "10 V", "100 V", "1 kV"]
dcv_range_val=["Auto", 1E-1, 1, 1E1, 1E2, 1E3]
dci_range=["AUTO ON", "10 μA", "100 μA", "1 mA", "10 mA" "100 mA", "1 A", "10 A", "30 A"]
dci_range_val=["AUTO ON", 1E-7, 10E-7, 1E-3, 10E-3, 100E-3, 1, 1E1, 3E1]
dc_digit_val=[4, 5, 6, 7, 8]
ac_digit_val=[4, 5, 6, 7]
dcv_zin=["Auto", "10 MΩ", "1 MΩ"]
VALID_RESOLUTIONS_DC = {1e-4, 1e-5, 1e-6, 1e-7, 1e-8}
auto_fast_values=[1E-2, 1E-1, 1, 1E1, 1E2] #values for autofast at 4, 5, 6, 7 8 digits of resolution

def getFunctions():
    return functions

def getDcvRange():
    return dcv_range

def getDciRange():
    return dci_range

def getDcvZin():
    return dcv_zin

def getDcvRangeVal(value):
    return dcv_range_val[dcv_range.index(value)]

def getDciRangeVal(value):
    return dcv_range_val[dci_range.index(value)]

def getDcDigitVal():
    return dc_digit_val

def getAcDigitVal():
    return ac_digit_val
