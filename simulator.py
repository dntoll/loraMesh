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
for i in range(3):
    sv = SimView(str(i) + ": ")
    x = i
    socket = SimulatorSocket(i, x, y)
    radio.add(socket)

    clients.append(PymeshAdapter(sv, socket, fpi))

clients[0].sendMessage(2, b"hello")
clients[2].sendMessage(0, b"hello")

for i in range(5):
    
    radio.process()
    sleep(1)
print("ended tests")

fpi.die()
print("tried to release threads")