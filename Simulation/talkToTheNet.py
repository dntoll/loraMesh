import sys
import os
cwd = os.getcwd()
sys.path.append(cwd + "\\MeshTestConsole")




from meshlibrary.PymeshAdapter import PymeshAdapter
from simulator.SimulatorSocket import SimulatorSocket
from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.SimTestView import SimTestView
from meshlibrary.Message import Message
from view.SerialConsoleView import SerialConsoleView

radio = Radio()
fpi = FakePycomInterface()

y = 0
clients = []
views = {}
for i in range(25):
    views[i] = SimTestView(i)
    if i == 0:
        views[i] = SerialConsoleView()
    x = i/5
    y = i/5
    socket = SimulatorSocket(i, x, y)
    radio.add(i, socket)
    clients.append(PymeshAdapter(views[i], socket, fpi))

c = MeshTestConsole()