import pycom
import time

class RGBView:

    RED = 0xFF0000
    GREEN = 0x00FF00
    BLUE = 0x0000FF
    WHITE = 0xFFFFFF
    

    def __init__(self):
        pycom.heartbeat(False)
    
    def receiveMessages(self, messages):
        self._blink(1, self.BLUE)

    def receiveMessageToMe(self, message):
        self._blink(1, self.RED)

    def receiveAccToMe(self, message):
        self._blink(1, self.WHITE)

    def sendMessage(self, message):
        self._blink(3, self.GREEN)
  
    def showIps(self, ips):
        return
    
    def update(self, pymeshAdapter):
        return

    def _blink(self, times, color):
        for _ in range(times):
            pycom.rgbled(color)
            time.sleep(.2)
            pycom.rgbled(0)
            time.sleep(.1)