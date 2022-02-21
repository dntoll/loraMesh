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


def test_testNodeGetsRemoved():
    st = SimTest()
    st.add(1, 0, 0)
    st.add(2, 1, 0)
    st.send(1, 2, b"h")
    st.wait(10)

    st.assertHasMessage(1, Message.TYPE_FIND)
    st.assertHasMessage(2, Message.TYPE_FIND)
    st.assertHasMessage(1, Message.TYPE_ACC)
    
    st.disableRadio(2)
    st.clearMessages(1)

    st.send(1, 2, b"m")
    st.wait(10)
    st.assertHasMessage(1, Message.TYPE_MESSAGE)
    st.assertHasNoMessage(1, Message.TYPE_ACC)

    st.endSim()


def test_alternatePathWhenNodeGetsRemoved():
    st = SimTest()
    st.add(1, 0, 0)
    st.add(2, 1, 0)
    st.add(3, 2, 0)

    #Send a message through relay, then replace the relay
    st.send(1, 3, b"h")
    st.wait(10)    
    st.disableRadio(2) #ONE RELAY IS REMOVED
    st.add(4, 1, 0) # THIS REPLACES LOST NODE
    st.clearMessages(1)
    st.clearMessages(3)

    st.send(1, 3, b"m")
    st.wait(10)
    #st.assertHasMessage(1, Message.TYPE_FIND) We might not want to specify how this happens
    st.assertHasMessage(3, Message.TYPE_FIND)
    st.assertHasMessage(1, Message.TYPE_ACC)

    st.endSim()

def test_firstRelayIsReplaced():
    st = SimTest()
    st.add(1, 0, 0)
    st.add(2, 1, 0)
    st.add(3, 2, 0)
    st.add(4, 3, 0)

    st.send(1, 4, b"h")
    st.wait(10)
    st.disableRadio(2) #First RELAY IS REMOVED
    st.add(5, 1, 0) #Replace lost node

    st.assertHasMessage(4, Message.TYPE_FIND)
    st.assertHasMessage(1, Message.TYPE_ACC)
    st.endSim()

def test_secondRelayIsReplaced():
    st = SimTest()
    st.add(1, 0, 0)
    st.add(2, 1, 0)
    st.add(3, 2, 0)
    st.add(4, 3, 0)

    st.send(1, 4, b"h")
    st.wait(10)
    st.disableRadio(3) #ONE RELAY IS REMOVED
    st.add(5, 2, 0) #Replace lost node

    st.assertHasMessage(4, Message.TYPE_FIND)
    st.assertHasMessage(1, Message.TYPE_ACC)
    st.endSim()    

def test_secondMessageHasRoute():
    st = SimTest()

    st.add(1, 0, 0)
    st.add(2, 1, 0)
    st.add(3, 2, 0)

    st.send(1, 3, b"h")
    st.wait(8)

    st.assertHasMessage(1, Message.TYPE_FIND)
    st.assertHasMessage(2, Message.TYPE_FIND)
    st.assertHasMessage(1, Message.TYPE_ACC)

    st.send(1, 3, b"b")
    st.wait(8)

    #st.assertHasMessage(1, Message.TYPE_MESSAGE) We may not want to specify
    st.assertHasMessage(2, Message.TYPE_MESSAGE)
    st.assertHasMessage(1, Message.TYPE_ACC)
    st.endSim()


def test_sendBetweenTwoCloseNodes():
    st = SimTest()
    st.add(1, 0, 0) #nodeIndex, xpos, ypos
    st.add(2, 1, 0)

    st.send(1, 2, b"h")
    st.wait(5)
    st.assertHasMessage(2, Message.TYPE_FIND)
    st.assertHasMessage(1, Message.TYPE_ACC)
    st.endSim()

def test_sendBeteweenRelayNodes():
    st = SimTest()
    st.add(1, 0, 0)
    st.add(2, 1, 0)
    st.add(3, 2, 0)

    st.send(1, 3, b"h")
    st.wait(8)
    st.assertHasMessage(3, Message.TYPE_FIND)
    st.assertHasMessage(1, Message.TYPE_ACC)
    st.endSim()

def test_sendBetweenFourNodes():
    st = SimTest()
    st.add(1, 0, 0)
    st.add(2, 1, 0)
    st.add(3, 2, 0)
    st.add(4, 3, 0)

    st.send(1, 4, b"h")
    st.wait(10)
    st.assertHasMessage(4, Message.TYPE_FIND)
    st.assertHasMessage(1, Message.TYPE_ACC)
    st.endSim()



def test_testNodeIsTooFarAway():
    st = SimTest()
    st.add(1, 0, 0)
    st.add(2, 2, 0)

    st.send(1, 2, b"h")
    st.wait(10)

    st.assertHasMessage(1, Message.TYPE_FIND)
    st.assertHasNoMessage(2, Message.TYPE_FIND)
    st.assertHasNoMessage(1, Message.TYPE_ACC)
    
    st.endSim()
