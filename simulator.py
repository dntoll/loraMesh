from mesh.PymeshAdapter import PymeshAdapter

from view.CompositeView import CompositeView

from simulator.SimulatorSocket import SimulatorSocket
from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.SimView import SimView
from simulator.SimTest import SimTest
from mesh.Message import Message
from time import sleep

"""
view = CompositeView()
radio = Radio()
fpi = FakePycomInterface()

y = 0
clients = []
for i in range(25):
    sv = SimView(i)
    x = i/5
    y = i/5
    socket = SimulatorSocket(i, x, y)
    radio.add(socket)
    clients.append(PymeshAdapter(sv, socket, fpi))

clients[0].sendMessage(3, b"first")
#clients[2].sendMessage(0, b"hello")

timePerStep = 0.01
oneTime = True

for i in range(int(10.0/timePerStep)):
    radio.process()
    sleep(timePerStep)
    if oneTime and i > int(5/timePerStep):
        print("Send")
        oneTime = False
        clients[3].sendMessage(0, b"firest")
print("ended tests")

fpi.die()
print("tried to release threads")

print(radio.sends)
"""
st = SimTest()
st.add(1, 0, 0)
st.add(2, 1, 0)

st.send(1, 2, b"h")
st.wait(0.2)
st.assertListen(2, Message.TYPE_FIND, b"h")
st.assertListen(1, Message.TYPE_ACC, b"h")
st.endSim()

st = SimTest()
st.add(1, 0, 0)
st.add(2, 1, 0)
st.add(3, 2, 0)

st.send(1, 3, b"h")
st.wait(0.2)
st.assertListen(2, Message.TYPE_FIND, b"h")
st.assertListen(1, Message.TYPE_ACC, b"h")
st.endSim()
