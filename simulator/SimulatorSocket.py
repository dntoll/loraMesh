
class SimulatorSocket:
	
	
	def __init__(self, mac):
		self.mac = mac
		self.sendBuffer = bytearray(b"")
		self.receiveBuffer = bytearray(b"")
        
	def send(self, bytes):
		
		for i in bytes:
			self.sendBuffer.append(i)
		return
        
	def receive(self):
		rec = bytes(self.receiveBuffer)
		self.receiveBuffer = bytearray(b"")
		return (rec, {"rssi" : -50})

	def getMac(self):
		return self.mac