
globalRadioBuffer = "";

class SimulatorSocket:
	
	
	def __init__(self, mac):
		self.mac = mac
        
	def send(self, bytes):
		globalRadioBuffer += bytes
		return
        
	def receive(self):
		global globalRadioBuffer 
		return (globalRadioBuffer, {})

	def getMac(self):
		return self.mac