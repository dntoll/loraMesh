import ftpdeploy
import pycom

pycom.pybytes_on_boot(False)
pycom.heartbeat(False)

from MeshTestConsole import MeshTestConsole
from meshlibrary.MeshFacade import MeshFacade
from meshlibrary.PycomInterface import PycomInterface

from view.CompositeView import CompositeView
from view.SerialConsoleView import SerialConsoleView


view = CompositeView()
#self.view.add(RGBView())
view.add(SerialConsoleView())
mf = MeshFacade(view, MeshTestConsole.callback)
        
a = MeshTestConsole(mf, view, PycomInterface())
a.run()

print("Release 3")
