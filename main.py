import pycom

pycom.pybytes_on_boot(False)

from AppController import AppController
from mesh.Message import Message

import socket


print("Release 1")

Message.test()

a = AppController()
a.run()

def p():
    global a
    a.pm.sendMessage(52, b"Ping")


