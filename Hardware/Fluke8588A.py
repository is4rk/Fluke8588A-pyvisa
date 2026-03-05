import pyvisa
import logging
from Config_Data.spin_box_values import VALID_RESOLUTIONS_DC
#CLASSE DEL DMM Fluke 8588A
class Fluke8588A(object):
	"""
	Class for communicating with Fluke 8588A DMM
	
	Public Methods:
	identify() : returns read value of *IDN? query
	write(text) : writes command to instrument
	query(text) : write and read in a single command
	read() : outputs measurement with ":READ?" query
	reset() : resets instrument to power on settings
	close() : close the connection
	
	Configuration Methods:
	init_dcv(range, resolution, zin, measure_mode, nplc) : initialize DC voltage mode
	setRange(root, value) / getRange(root) : set/get measurement range
	setResolution(root, value) / getResolution(root) : set/get resolution
	setNplc(root, value) / getNplc(root) : set/get NPLC value (1plc=50Hz in EU)
	setImpedence(root, value) / getImp(root) : set/get input impedance
	"""

	def __init__(self, address):
		logging.info(__name__ + ' : Initializing instrument Fluke 8588A')
		try:
			self.__connect(address)
			self._instr.timeout = 10e3
			self.plc_max = 500
			self.reset()
			idn_string = self.identify()
		except pyvisa.VisaIOError:
			print("Instrument not detected. Check GPIB address!")
		print("\nInstrument %s successfully initialized. \n" % idn_string)

	def __connect(self, address): #private to be only used by init
		rm = pyvisa.ResourceManager()
		self._address = address
		self._instr = rm.open_resource("GPIB0::" + str(self._address) + "::INSTR")
		
	def identify(self):
		'''
		Sends query *IDN?
		Input:
			none
		Output:
			machine identifiers 
		'''
		return self.query("*IDN?")

	def write(self, text):
		'''
		Write function
		Input:
			command text
		Output:
			none
		'''  
		self._instr.write(text)


	def query(self, text):
		'''
		Query function
		Input:
			command text
		Output:
			text
		'''  
		return self._instr.query(text)
		
	
	def read(self):
		'''
		Read function
		Input:
			none
		Output:
			text
		'''  
		return self.query(":READ?")
						
	def reset(self):
		'''
		Return Fluke 8588A to power up state...
		Input:
			none
		Output:
			none
		'''        
		self.write("*RST")
	
	def close(self):
		'''
		Closes connection with machine
		Input:
			none
		Output:
			none
		'''
		self._instr.close()

	def init_dcv(self, range, resolution, zin, measure_mode, nplc):
		'''
		Set the machine to dcv mode, and set up parameters
		'''
		root=":VOLT:DC"
		self.write(":FUNC \":VOLT:DC\"")
		self.setRange(root, range)
		self.setResolution(root, resolution)
		self.setImpedence(root, zin)
		self.setNplc(root, nplc)

	def getApertureMode(self, root):
		'''
		Get aperture mode for given root
		Input:
			Root
		Output:
			"AUTO", "FAST", "MAN"
		'''
		return self.query(root+":APER:MODE?")
	def setApertureMode(self, root, value):
		'''
		Get aperture mode for given root
		Input:
			Root, desired value "AUTO", "FAST", "MAN
		Output:
			set value: "AUTO", "FAST", "MAN"
		'''
		self.write(root+":APER:MODE:"+str(value))
		return self.getApertureMode(root)
	
	def getNplc(self, root):
		'''
		Get Nplc value for given root
		Input:
			root
		Output:
			set value
		'''
		return self.query(root+":NPLC?")
	def setNplc(self, root, value):
		'''
		Set NPLC value for given root
		Input:
			root, desired value
		Output:
			set value
		'''
		self.write(root+":NPLC "+str(value))
		return self.getNplc(root)

	def getImp(self, root):
		'''
		Get Impedence value for given root
		Input:
			root
		Output:
			set value
		'''
		return self.query(root+":IMP?")
	def setImpedence(self, root, value):
		'''
		Set Impedence value for given root
		Input:
			root, desired value
		Output:
			set value
		'''
		self.write(root+":IMP "+str(value))
		return self.getImp(root)
	
	def getRange(self, root):
		'''
		Get range value for given root
		Input:
			root
		Output:
			set value
		'''
		return self.query(root+":RANG?")
	def setRange(self, root, value):
		'''
		Set range value for given root
		Input:
			root, desired value
		Output:
			set value
		'''
		self.write(root+":RANG "+str(value))
		return self.getRange(root)
	
	def getResolution(self, root):
		'''
		Get resolution value for given root
		Input:
			root
		Output:
			set value
		'''
		return self.query(root+":RES?")
	
	def setResolution(self, root, value):
		'''
		Set number of digits after 0 to measure, for a given root
		Input:
			root, int value
		Output:
			set value

		Example:
			setResolution(":VOLT:DC", 4)-->1.2348 V
			setResolution(":VOLT:DC", "4")-->1.2348 V
			setResolution(":VOLT:DC", 6)-->1.234778 V
		'''
		converted_resolution = self.__convert_resolution(int(value))
		self.write(root+":RES "+str(converted_resolution))
		set_resolution=self.getResolution(root)
		return self.__anti_convert_resolution(set_resolution)
	
	def __convert_resolution(self, value):
		return 10**(-value)

	# Fluke for 4 digit precision returns 1E-4, python can do errors in saving the value, so this function returns how many points of precision after the zero the machine is saving. To do so, given 1E-4 that might get saved as 0.0001000005, the program counts how many zeros are present from . to 1. In this case there are 3 zeros, so the machine is measuring 4 digit precision 
	def __anti_convert_resolution(self, value):
		value = f"{float(value):.17f}"
		after_decimal_point=list(str(value).split(".")[1]) #takes 1.00200000003 -> [0, 0, 2, 0, 0, ..., 3]
		i=1
		for digit in after_decimal_point:
			if digit=='1': 
				return i
			elif digit=='0':
				i+=1
			else: # Machine/SCPI error
				raise ValueError(f"Unexpected resolution from instrument: {value}. Expected one of {VALID_RESOLUTIONS_DC}")