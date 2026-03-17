from dataclasses import dataclass

@dataclass
class DcvSettings:
    range_mode: str
    range_val:  str
    resolution: int
    zin:        str
    aperture_mode: str
    time:       float 
