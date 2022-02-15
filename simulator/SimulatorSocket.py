import threading
import math
from collections import namedtuple

class SimulatorSocket:
	
	
	def __init__(self, mac, posx, posy):
		self.mac = mac
		self.sendBuffer = bytearray(b"")
		self.receiveBuffer = bytearray(b"")
		self.lock = threading.Lock()
		self.posx = posx
		self.posy = posy
        
	def send(self, bytes):
		self.lock.acquire()
		for i in bytes:
			self.sendBuffer.append(i)
		
		self.lock.release()
		return
        
	def receive(self):
		self.lock.acquire()
		rec = bytes(self.receiveBuffer)
		self.receiveBuffer = bytearray(b"")
		self.lock.release()

		Stats = namedtuple("Stats", "rssi")
		return (rec, Stats(-50))

	def getMac(self):
		return self.mac

	def clearSendBuffer(self):
		self.lock.acquire()
		self.sendBuffer = bytearray(b"")
		self.lock.release()
	
	def fillReceiveBuffer(self, content):
		self.lock.acquire()
		for i in content:
			self.receiveBuffer.append(i)
		self.lock.release()

	def inRange(self, other):

		distx = (self.posx - other.posx)**2
		disty = (self.posy - other.posy)**2

		return math.sqrt(distx+disty) <= 2.1



