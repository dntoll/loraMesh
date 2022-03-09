import sys
import os
cwd = os.getcwd()
sys.path.append(cwd + "\\MeshTestConsole")

from simulator.SimulatorSocket import SimulatorSocket
from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.SimTest import SimTest
from meshlibrary.Message import Message
from time import sleep


def test_MessageTests():
    Message.test()

def test_testNodeGetsRemoved():
    st = SimTest()
    st.add(1, 0, 0)
    st.add(2, 1, 0)
    st.send(1, 2, b"h")
    st.processUntilSilent(0.3)

    st.assertHasMessage(1, Message.TYPE_FIND)
    st.assertHasMessage(2, Message.TYPE_FIND)
    st.assertHasMessage(1, Message.TYPE_ACC)
    
    st.disableRadio(2)
    st.clearMessages(1)

    st.send(1, 2, b"m")
    st.processUntilSilent(0.3)
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
    st.processUntilSilent(0.3)
    st.disableRadio(2) #ONE RELAY IS REMOVED
    st.add(4, 1, 0) # THIS REPLACES LOST NODE
    st.clearMessages(1)
    st.clearMessages(3)

    st.send(1, 3, b"m")
    st.processUntilSilent(0.3)
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
    st.processUntilSilent(0.3)
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
    st.processUntilSilent(0.3)
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
    st.processUntilSilent(0.3)

    st.assertHasMessage(1, Message.TYPE_FIND)
    st.assertHasMessage(2, Message.TYPE_FIND)
    st.assertHasMessage(1, Message.TYPE_ACC)

    st.send(1, 3, b"b")
    st.processUntilSilent(0.3)

    #st.assertHasMessage(1, Message.TYPE_MESSAGE) We may not want to specify
    st.assertHasMessage(2, Message.TYPE_MESSAGE)
    st.assertHasMessage(1, Message.TYPE_ACC)
    st.endSim()


def test_sendBetweenTwoCloseNodes():
    st = SimTest()
    st.add(1, 0, 0) #nodeIndex, xpos, ypos
    st.add(2, 1, 0)

    st.send(1, 2, b"h")
    st.processUntilSilent(0.3)
    st.assertHasMessage(2, Message.TYPE_FIND)
    st.assertHasMessage(1, Message.TYPE_ACC)
    st.endSim()

def test_sendBeteweenRelayNodes():
    st = SimTest()
    st.add(1, 0, 0)
    st.add(2, 1, 0)
    st.add(3, 2, 0)

    st.send(1, 3, b"h")
    st.processUntilSilent(0.3)
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
    st.processUntilSilent(0.3)
    st.assertHasMessage(4, Message.TYPE_FIND)
    st.assertHasMessage(1, Message.TYPE_ACC)
    st.endSim()



def test_testNodeIsTooFarAway():
    st = SimTest()
    st.add(1, 0, 0)
    st.add(2, 2, 0)

    st.send(1, 2, b"h")
    st.processUntilSilent(0.3)

    st.assertHasMessage(1, Message.TYPE_FIND)
    st.assertHasNoMessage(2, Message.TYPE_FIND)
    st.assertHasNoMessage(1, Message.TYPE_ACC)
    
    st.endSim()
