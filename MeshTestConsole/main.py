import ftpdeploy
import pycom

pycom.pybytes_on_boot(False)
pycom.heartbeat(False)

from meshlibrary.MeshFacade import MeshFacade
from MeshTestConsole import MeshTestConsole
from view.CompositeView import CompositeView
from view.SerialConsoleView import SerialConsoleView
from meshlibrary.PycomInterface import PycomInterface


view = CompositeView()
#view.add(RGBView())
view.add(SerialConsoleView())

a = MeshTestConsole(view= view, hardwareInterface = PycomInterface(), meshFacade = MeshFacade(view, MeshTestConsole.callback))
a.run()

print("Release 3")


