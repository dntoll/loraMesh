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

def devNullCallback(origin, content):
    #print("Content: " + content)
    return

for i in range(25):
    views[i] = CompositeView()
    nodeCallBack = devNullCallback
    if i == 0:
        views[i] = SerialConsoleView()
        nodeCallBack = MeshTestConsole.callback
    x = i/5
    y = i%5
    socket = SimulatorSocket(i, x, y)
    radio.add(i, socket)
    clients[i] = PymeshAdapter(views[i], socket, fpi, nodeCallBack)



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
    ch = input("Input command master [#] Send from 0 to # node ID, [Q]uit], [S]:")
    if ch:
        if ch.isnumeric():
            clients[0].sendMessage(int(ch), b"Message")
        elif ch == "Q":
            break
        elif ch == "S":
            s = input("Input Sender #:")
            t = input("Input Target #:")
            m = input("Input Message :")
            clients[int(s)].sendMessage(int(t), m.encode('utf-8'))
            
