import threading
import time
import random
from time import sleep



class FakePycomInterface:
	def __init__(self):
		self.threads = []

	def allocate_lock(self):
		return threading.Lock()
        

	def start_new_thread(self,listener, toThread):
		t = threading.Thread(target=listener, args=toThread, daemon=True)

		self.threads.append(t)
		t.start() 

	def ticks_ms(self):
		return round(time.time() * 1000)

	def rng(self):
		return random.randint(0, 1000)

	def sleep_ms(self, millis):
		sleep(millis / 1000)

	def die(self):
		for n in self.threads:
			n.join(0)