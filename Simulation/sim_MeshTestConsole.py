from msilib.schema import Component
import sys
import os
cwd = os.getcwd()
sys.path.append(cwd + "\\MeshTestConsole")
import threading



from meshlibrary.PymeshAdapter import PymeshAdapter
from simulator.SimulatorSocket import SimulatorSocket
from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.SimTestView import SimTestView
from simulator.FakePycomInterface import FakePycomInterface

from meshlibrary.Message import Message
from view.SerialConsoleView import SerialConsoleView
from view.CompositeView import CompositeView
from MeshTestConsole import MeshTestConsole
from time import sleep

radio = Radio()
fpi = FakePycomInterface()

y = 0
clients = {}
views = {}
for i in range(25):
    views[i] = CompositeView()
    if i == 0:
        views[i] = SerialConsoleView()
    x = i/5
    y = i%5
    socket = SimulatorSocket(i, x, y)
    radio.add(i, socket)
    clients[i] = PymeshAdapter(views[i], socket, fpi)



c = MeshTestConsole(views[0], FakePycomInterface(), clients[0])
c.run()

def radioThreadFunc(radio, c):
    while True:
        radio.process()
        sleep(0.5)
        print(end="", flush=True)

t = threading.Thread(target=radioThreadFunc, args=(radio, c), daemon=True)
t.start() 


while True:
    sleep(0.1)
    ch = input("Input command master [#] Send to # node ID, [Q]uit]:")
    if ch:
        if ch.isnumeric():
            clients[0].sendMessage(int(ch), b"Message")
        elif ch == "Q":
            break
