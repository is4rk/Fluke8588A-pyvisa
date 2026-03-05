import pyvisa
import logging
from config import InstrumentConfig
#CLASSE DEL DMM Fluke 8588A
class Fluke8588A():
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
	init_dcv(range_mode, range_val, resolution_val, zin_val, aperture_mode, nplc_val) : initialize DC voltage mode
	setRange(root, value) / getRange(root) : set/get measurement range
	setResolution(root, value) / getResolution(root) : set/get resolution
	setNplc(root, value) / getNplc(root) : set/get NPLC value (1plc=50Hz in EU)
	setImpedence(root, value) / getImp(root) : set/get input impedance
	setRangeMode(root, value) / getRangeMode(root) : set/get range mode ("AUTO" or "MAN")
	setApertureMode(root, value) / getApertureMode(root) : set/get aperture mode ("AUTO", "FAST", or "MAN")
	"""

	def __init__(self, address):
		logging.info(__name__ + ' : Initializing instrument Fluke 8588A')
		self.__connect(address)
		self._instr.timeout = InstrumentConfig.TIMEOUT_MS
		self.plc_max = InstrumentConfig.PLC_MAX
		self.reset()
		idn_string = self.identify()
		logging.info("Instrument %s successfully initialized." % idn_string)

	def __connect(self, address): #private to be only used by init
		rm = pyvisa.ResourceManager()
		self._address = address
		self._instr = rm.open_resource(InstrumentConfig.GPIB_PREFIX + str(self._address) + InstrumentConfig.GPIB_SUFFIX)
		
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

	def init_dcv(self, range_mode, range_val,  resolution_val, zin_val, aperture_mode, nplc_val):
		'''
		Set the machine to dcv mode, and set up parameters
		'''
		root=InstrumentConfig.ROOT_DCV
		self.write(":FUNC \"" + root + "\"")
		self.setRangeMode(root, range_mode)
		self.setRange(root, range_val)
		self.setResolution(root, resolution_val)
		self.setImpedence(root, zin_val)		
		self.setApertureMode(root, aperture_mode)
		self.setNplc(root, nplc_val)

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
		Sets aperture mode for given root.
		Input:
			root  : SCPI root string e.g. ":VOLT:DC"
			value : "AUTO", "FAST", or "MAN"
		Output:
			set value: "AUTO", "FAST", or "MAN"
		'''
		if value not in InstrumentConfig.VALID_APERTURE_MODES:
			raise ValueError(
				f"Invalid aperture mode '{value}'. "
				f"Expected one of {InstrumentConfig.VALID_APERTURE_MODES}"
			)
		self.write(root + ":APER:MODE " + str(value))
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
		Sets NPLC value for given root.
		1 PLC = 20ms at 50Hz (EU).
		Input:
			root  : SCPI root string e.g. ":VOLT:DC"
			value : float between 0.001 (20μs) and 500 (10s)
		Output:
			set value as string
		'''
		if not InstrumentConfig.NPLC_MIN <= float(value) <= InstrumentConfig.PLC_MAX:
			raise ValueError(
				f"NPLC must be between {InstrumentConfig.NPLC_MIN} "
				f"and {InstrumentConfig.PLC_MAX}, got {value}"
			)
		self.write(root + ":NPLC " + str(value))
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
		Sets input impedance for given root.
		Input:
			root  : SCPI root string e.g. ":VOLT:DC"
			value : "AUTO", "1M", or "10M"
		Output:
			set value: "AUTO", "1M", or "10M"
		'''
		if value not in InstrumentConfig.VALID_IMPEDANCES_DCV:
			raise ValueError(
				f"Invalid impedance '{value}'. "
				f"Expected one of {InstrumentConfig.VALID_IMPEDANCES_DCV}"
			)
		self.write(root + ":IMP " + str(value))
		return self.getImp(root)
	

	def getRangeMode(self, root):
		'''
		Get range mode for given root
		Input:
			root, value
		Output:
			"AUTO" or "MAN"
		'''
		response = self.query(root+":RANG:AUTO?")
		value_int = int(float(response))
		if value_int == InstrumentConfig.RANGE_MODE_AUTO:
			return InstrumentConfig.RANGE_MODE_AUTO_STR
		elif value_int == InstrumentConfig.RANGE_MODE_MAN:
			return InstrumentConfig.RANGE_MODE_MAN_STR
		else:
			raise ValueError(f"Unexpected range mode value: {response}")
	def setRangeMode(self, root, value):
		'''
		Sets range mode for given root.
		Input:
			root  : SCPI root string e.g. ":VOLT:DC"
			value : "AUTO" or "MAN"
		Output:
			set value: "AUTO" or "MAN"
		'''
		if value == InstrumentConfig.RANGE_MODE_AUTO_STR:
			converted_value = InstrumentConfig.RANGE_MODE_AUTO
		elif value == InstrumentConfig.RANGE_MODE_MAN_STR:
			converted_value = InstrumentConfig.RANGE_MODE_MAN
		else:
			raise ValueError(
				f"Invalid range mode '{value}'. "
				f"Expected '{InstrumentConfig.RANGE_MODE_AUTO_STR}' "
				f"or '{InstrumentConfig.RANGE_MODE_MAN_STR}'"
			)
		self.write(root + ":RANG:AUTO " + str(converted_value))
		return self.getRangeMode(root)
	

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
		Sets resolution in digits for given root.
		Converts digit count to the resolution value the instrument expects.
		Input:
			root  : SCPI root string e.g. ":VOLT:DC"
			value : int or str, number of digits (4–8 for DC, 4–7 for AC)
		Output:
			set value in digits (int)

		Example:
			setResolution(":VOLT:DC", 4) --> measures 1.2348 V  (returns 4)
			setResolution(":VOLT:DC", 6) --> measures 1.234778 V (returns 6)
		'''
		digit_value = int(value)
		is_ac = "AC" in root.upper()
		
		if is_ac:
			if digit_value not in InstrumentConfig.VALID_RESOLUTIONS_AC_DIGITS:
				raise ValueError(
					f"AC resolution must be one of {InstrumentConfig.VALID_RESOLUTIONS_AC_DIGITS}, got {digit_value}"
				)
		else:
			if digit_value not in InstrumentConfig.VALID_RESOLUTIONS_DC_DIGITS:
				raise ValueError(
					f"DC resolution must be one of {InstrumentConfig.VALID_RESOLUTIONS_DC_DIGITS}, got {digit_value}"
				)
		
		converted_resolution = self.__convert_resolution(digit_value)
		self.write(root + ":RES " + str(converted_resolution))
		set_resolution = self.getResolution(root)
		return self.__anti_convert_resolution(set_resolution)
	
	def __convert_resolution(self, value):
		return 10**(-value)

	# Fluke returns resolution as a float e.g. 1E-4.
	# Python floating point may store this as 0.00010000000000000005.
	# This function recovers the digit count by counting leading zeros after
	# the decimal point until the first '1' is found.
	def __anti_convert_resolution(self, value):
		formatted = f"{float(value):.17f}"
		after_decimal = formatted.split(".")[1]
		for i, digit in enumerate(after_decimal, start=1):
			if digit == '1':
				return i
			elif digit != '0':
				raise ValueError(
					f"Unexpected resolution from instrument: {value}. "
				)
		raise ValueError(
			f"No significant digit found in resolution value: {value}"
		)