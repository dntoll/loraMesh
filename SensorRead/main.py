import pycom
pycom.pybytes_on_boot(False)
pycom.heartbeat(False)

from meshlibrary.MeshFacade import MeshFacade
from meshlibrary.BaseView import BaseView
from dht import DHTHelper
import time

view = BaseView()


def callback(originIP, contentBytes):
        print("Received Temp: " + str(contentBytes[0]) + " from " + str(originIP))
        print("Received Hum: " + str(contentBytes[1]) + " from " + str(originIP))
        return

meshFacade = MeshFacade(view, callback)

print("Started app")


if meshFacade.getMyAddress() == 102:
    dhtsensor = DHTHelper('P23')

    while True:
        readBytes = dhtsensor.readBytes()

        meshFacade.sendMessage(52, readBytes)
        time.sleep(10)


