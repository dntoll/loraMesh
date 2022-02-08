import threading
import time
import random
from time import sleep



class FakePycomInterface:


	def allocate_lock(self):
		return threading.Lock()
        

	def start_new_thread(self,listener, toThread):
		t = threading.Thread(target=listener, args=toThread)
		t.start() 

	def ticks_ms(self):
		return round(time.time() * 1000)

	def rng(self):
		return random.randint(0, 1000)

	def sleep_ms(self, millis):
		sleep(millis / 1000)