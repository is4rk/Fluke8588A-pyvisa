# Fluke8588A-pyvisa
A Python library (in development for INRIM) to control the Fluke 8588A high‑precision digitizer / DMM through pyvisa.

It will work with direct ethernet, GPIB, and USB. Will try to implement remote communication.

# Structure
There exist two categories of files:
- Fluke8588A library files:
  - FLuke8588A.py
  - SpinBoxValues.py 
- GUI
  - uiinterface.py
  - mainwindow.ui
  - measSetupDc.ui

The Fluke8588A library files category is stand alone, so if you want to implement your own script or interface, does are sufficient.
The GUI files present a GUI interface in English, all files from both  categories are needed to run the interface.
