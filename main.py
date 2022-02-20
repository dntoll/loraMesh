import pycom

pycom.pybytes_on_boot(False)
pycom.heartbeat(False)

from AppController import AppController
from mesh.Message import Message
from mesh.Route import Route

import socket
import network 
from network import WLAN
import machine
import time
import secrets


pycom.pybytes_on_boot(False)
pycom.smart_config_on_boot(False)
pycom.wifi_on_boot(True)
pycom.wifi_mode_on_boot(WLAN.STA)
pycom.wifi_ssid_sta(secrets.ssid)
pycom.wifi_pwd_sta(secrets.pwa)
wlan = network.WLAN(mode=network.WLAN.STA)
print(wlan.ifconfig())

print("Release 1")

Message.test()

a = AppController()
a.run()

def p():
    global a
    a.pm.sendMessage(52, b"Ping")

def rp():
    global a
    m = Message(54, Route(bytes((54,102, 101))), Message.TYPE_MESSAGE, b"Routethis")
    a.pm.meshController.addToQue(m)


