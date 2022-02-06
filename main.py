import pycom

pycom.pybytes_on_boot(False)
pycom.heartbeat(False)

from AppController import AppController
from mesh.Message import Message
from mesh.Route import Route

import socket


print("Release 1")

Message.test()

a = AppController()
a.run()

def p():
    global a
    a.pm.sendMessage(52, b"Ping")

def rp():
    global a
    m = Message(13, Route.fromBytes(bytes((13,14, 52,50))), Message.TYPE_MESSAGE, b"Routethis")
    a.pm.meshController.addToQue(m)


