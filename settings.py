from dataclasses import dataclass

@dataclass
class DcvSettings:
    range_val:  str
    resolution: int
    zin:        str
    nplc:       float
