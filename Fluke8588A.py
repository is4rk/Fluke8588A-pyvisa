#CLASSE DEL DMM Fluke 8588A
class Fluke8588A(object):
	"""
	Class for communicating with 
	
	Setup the AWG I/O with GPIB
	
	identify() : returns read value of *IDN? query
	write(message) : writes to instrument, no return
	query(message) : write and read in a single command
	read() : outputs returned text or times out
	reset() : resets instrument to power on settings
	set_nplc() : sets nplc value (1nplc=50HZ in eu)
	read_voltage() : reads voltage value
	close() : close the connection

	
	"""
	"""inizializzazione"""
	def __init__(self, name, address):
		logging.info(__name__ + ' : Initializing instrument Fluke 8588A')

		#Instrument.__init__(self, name, tags=['physical'])
		rm = pyvisa.ResourceManager()
		self._address = address
		self._instr = rm.open_resource("GPIB0::" + str(self._address) + "::INSTR")
		self._instr.timeout = 10e3 #ms
		
		self.max_digits = 8
		self.nplc_max = 500

		try:
			self.write("*RST")
			idn_string = self.identify()
		except pyvisa.VisaIOError:
			print("Instrument not detected. Check GPIB address!")

		# self.write(":SENSE:VOLT:DC")
		# self.write(":SENSE:VOLT:DC:RANG:AUTO ON")        
		print("\nInstrument %s successfully initialized. \n" % idn_string)

	def identify(self):
		return self._instr.query("*IDN?")
		
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
		return self._instr.read()    
					
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
		
	# def set_digits(self, digits):
	# 	'''
	# 	Change digits
	# 	'''
	# 	if digits > self.max_digits: digits = self.max_digits
	# 	self._instr.write("NDIG %d" % int(digits))
		
		
	def set_nplc(self, nplc):
		'''
		Change NPLC value
		'''
		if nplc > self.nplc_max: nplc = self.nplc_max
		self._instr.write(":SENSE:VOLT:DC:NPLC %.3f" % nplc) 
 

	def read_voltage(self):
		'''
		Get a single voltage reading
		'''
		voltage = float(self.query("READ?"))
		return voltage

	def close(self):
		self._instr.close()

	
	# def read_bytes(self, nbytes):
	# 	"""Read the returned data"""
	# 	return self.dmm.read_bytes(nbytes)
	
#END CLASSE DEL DMM Fluke8588A
