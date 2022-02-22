import pycom

pycom.pybytes_on_boot(False)
pycom.heartbeat(False)

from MeshTestConsole import MeshTestConsole
from mesh.Message import Message
from mesh.Route import Route

import socket
import network 
from network import WLAN
import machine
import time
import secrets

#this part is to get the OTA update to work
pycom.pybytes_on_boot(False)
pycom.smart_config_on_boot(False)
pycom.wifi_on_boot(True)
pycom.wifi_mode_on_boot(WLAN.STA)
pycom.wifi_ssid_sta(secrets.ssid)
pycom.wifi_pwd_sta(secrets.pwa)
wlan = network.WLAN(mode=network.WLAN.STA)
#end of OTA

print(wlan.ifconfig())



Message.test()

a = MeshTestConsole()
a.run()

print("Release 3")




