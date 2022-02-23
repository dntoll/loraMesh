
import machine
import _thread
import utime
import time
import machine


class PycomInterface:


	def allocate_lock(self):
		return _thread.allocate_lock()
        

	def start_new_thread(self, listener, toThread):
		return _thread.start_new_thread(listener, toThread)

	def ticks_ms(self):
		return utime.ticks_ms()

	def rng(self):
		return machine.rng()


	def sleep_ms(self, millis):
		time.sleep_ms(millis)