import ftpdeploy
import pycom

pycom.pybytes_on_boot(False)
pycom.heartbeat(False)

from MeshTestConsole import MeshTestConsole

a = MeshTestConsole()
a.run()

print("Release 3")




