from mesh.PymeshAdapter import PymeshAdapter

from view.CompositeView import CompositeView

from simulator.SimulatorSocket import SimulatorSocket
from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.SimView import SimView
from time import sleep



view = CompositeView()
radio = Radio()
fpi = FakePycomInterface()

y = 0
clients = []
for i in range(25):
    sv = SimView(str(i) + ": ")
    x = i/5
    y = i/5
    socket = SimulatorSocket(i, x, y)
    radio.add(socket)

    clients.append(PymeshAdapter(sv, socket, fpi))

clients[0].sendMessage(4, b"first")
#clients[2].sendMessage(0, b"hello")

timePerStep = 0.05
oneTime = True

for i in range(int(30.0/timePerStep)):
    radio.process()
    sleep(timePerStep)
    if oneTime and i > int(10/timePerStep):
        print("Send")
        oneTime = False
        clients[0].sendMessage(2, b"second")
print("ended tests")

fpi.die()
print("tried to release threads")