import pyvisa
import logging
import SpinBoxValues as sbv
#CLASSE DEL DMM Fluke 8588A
class Fluke8588A(object):
	"""
	Class for communicating with  FLuke8588A
		
	identify() : returns read value of *IDN? query
	write(message) : writes to instrument, no return
	query(message) : write and read in a single command
	read() : outputs returned text or times out
	reset() : resets instrument to power on settings
	set_plc() : sets plc value (1plc=50HZ in eu)
	close() : close the connection
	"""
	"""initialization"""


	def __init__(self, address):
		logging.info(__name__ + ' : Initializing instrument Fluke 8588A')
		self.__connect(address)
		self._instr.timeout = 10e3
		self.plc_max = 500

		try:
			self.write("*RST")
			idn_string = self.identify()
		except pyvisa.VisaIOError:
			print("Instrument not detected. Check GPIB address!")

		# self.write(":SENSE:VOLT:DC")
		# self.write(":SENSE:VOLT:DC:RANG:AUTO ON")        
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
		return self._instr.query("*IDN?")
	
	'''does write(text)'''
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
					
	# class methods
	
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
		self._instr.close()

	def init_dcv(self, range, resolution, zin, measure_mode, nplc):
		'''
		Set the machine to dcv mode, and set up parameters
		'''
		root=":VOLT:DC"
		initStatus=[]
		self.write(":FUNC \":VOLT:DC\"")
		initStatus.append(self.setRange(root, range))
		initStatus.append(self.setResolution(root, resolution))
		initStatus.append(self.setImpedence(root, zin))
		initStatus.append(self.setNplc(root, measure_mode, nplc))

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
		self.write(root+":NPLC "+str((value)))
		return self.getNplc

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
		self.write(root+":IMP "+value)
		return self.getImp(root)
	
	def getRange(self, root):
		'''
		Get range value for given root
		Input:
			root
		Output:
			set value
		'''
		return int(self.query(root+":RANG?"))
	def setRange(self, root, value):
		'''
		Set range value for given root
		Input:
			root, desired value
		Output:
			set value
		'''
		self.write(root+":RANG: "+value)
		return self.getRange(root)
	
	def getResolution(self, root):
		'''
		Get resolution value for given root
		Input:
			root
		Output:
			set value
		'''
		return int(self.query(root+":RES?"))
	
	def setResolution(self, root, value):
		'''
		Get resolution value for given root
		Input:
			root
		Output:
			set value
		'''
		self.write(root+":RES "+value)
		return self.getResolution(root)