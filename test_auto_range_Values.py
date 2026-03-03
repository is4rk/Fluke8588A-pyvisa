import pyvisa
import SpinBoxValues as sbv
import Fluke8588A as flk

f=flk.__init__(9)
f.setRange("Auto")
f.setResolution("3")