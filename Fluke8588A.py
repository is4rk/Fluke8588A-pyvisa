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
		rm = pyvisa.ResourceManager()
		self._address = address
		self._instr = rm.open_resource("GPIB0::" + str(self._address) + "::INSTR")
		self._instr.timeout = 10e3
		self.max_digits = 8
		self.min_digits = 4
		self.plc_max = 500

		try:
			self.write("*RST")
			idn_string = self.identify()
		except pyvisa.VisaIOError:
			print("Instrument not detected. Check GPIB address!")

		# self.write(":SENSE:VOLT:DC")
		# self.write(":SENSE:VOLT:DC:RANG:AUTO ON")        
		print("\nInstrument %s successfully initialized. \n" % idn_string)
	'''returns *IDN?'''
	def identify(self):
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

	def set_plc(self, plc):
		'''
		Change PLC value
		'''
		if plc > self.plc_max: plc = self.plc_max
		self._instr.write(":SENSE:VOLT:DC:PLC %.3f" % plc) 
 
	def init_dcv(self, range, resolution, zin, plc):
		'''
		Set the machine to dcv mode, and set up parameters
		'''
		root_commands=":VOLT:DC"
		initStatus=[]
		self.write(":FUNC \":VOLT:DC\"")
		initStatus.append(self.setRange(root_commands, range))
		initStatus.append(self.setAperture(root_commands, aperture))
		initStatus.append(self.setPlc(root_commands, plc))
		initStatus.append(self.setImp(root_commands, imp_str))
		initStatus.append(self.setRangeAutomatic(root_commands, auto_aperture))

	def getAperture(self, root):
		return int(self.query(root+":APER?"))
	def getApertureMode(self, root):
		return str(self.query(root+":APER:MODE?"))
	
	def setAperture(self, root, value):
		try:
			value=float(value)
		except (ValueError, TypeError):
			print("the aperture variable variable has to be a number (int, float, or scientific notation)")
			return -1
		self.write(root+":APER "+str(value))
		return 0
	def setApertureMode(self, root ,value):
		try:
			if not value in sbv.getApertureMode():
				raise ValueError("aperture mode has to be AUTO FAST MAN")
		except (ValueError, TypeError):
			print("Aperture value error")
			return -1
		self.write(root+"APER:MODE "+value)
		return 0
	
	def getNplc(self, root):
		return self.query(root+":PLC?")

	def setNplc(self, root, value):
		try:
			self.write(root+":PLC "+str(float(value)))
		except (ValueError, TypeError):
			print("plc variable out of range")
			return -1
		return self.query(root+":PLC?")

	def getImp(self, root):
		return self.query(root+":IMP?")

	def setImp(self, root, value):
		try:
			if not value in sbv.getDcvZin():
				raise ValueError("impedance has to be AUTO 10M 1M")
		except (ValueError, TypeError):
			print("Impedance value error")
			return self.getImp(root)
		self.write(root+":IMP "+value)
		return self.getImp(root)

	
	# def getMax(self, root, branch):
	# 	return int(self.query(root+branch+"? MAX"))
	# def getMin(self, root, branch):
	# 	return int(self.query(root+branch+"? MIN"))
	# def getDef(self, root, branch):
	# 	return int(self.query(root+branch+":? DEF"))
	
	
	def getRange(self, root):
		"""returns set range"""
		return int(self.query(root+":RANG?"))
		
	def setRange(self, root, value):
		"""sets given range, return actual set range"""
		try:
			if (root == "DCV" and value not in sbv.getDcvRange()) or (root == "DCI" and value not in sbv.getDciRange()):				
				raise ValueError("range not in " + root +" range List")
		except:
			return self.getRange(root)
		self.write(root+":RANG: "+str(sbv.getDcvRangeVal(value)))
		return self.getRange(root)
		