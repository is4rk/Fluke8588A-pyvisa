functions=["DCV", "DCI", "ACV", "ACI", "OHMS", "DIGITIZE"]
dcv_range=["Auto", "100 mV", "1 V", "10 V", "100 V", "1 kV"]
dcv_range_val=[1E-1, 1, 1E1, 1E2, 1E3]
dci_range=["Auto", "10 μA", "100 μA", "1 mA", "10 mA" "100 mA", "1 A", "10 A", "30 A"]
dci_range_val=[1E-7, 10E-7, 1E-3, 10E-3, 100E-3, 1, 1E1, 3E1]

dcv_zin=["Auto", "10 MΩ", "1 MΩ"]

def getFunctions():
    return functions

def getDcvRange():
    return dcv_range

def getDciRange():
    return dci_range

def getDcvZin():
    return dcv_zin

def getDcvRangeVal(value):
    return dcv_range_val[dcv_range.index(value)-1]

def getDciRangeVal(value):
    return dcv_range_val[dci_range.index(value)-1]

