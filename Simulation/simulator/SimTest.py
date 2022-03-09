from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.SimTestView import SimTestView
from view.CompositeView import CompositeView

from simulator.SimulatorSocket import SimulatorSocket
from meshlibrary.PymeshAdapter import PymeshAdapter
from meshlibrary.Message import Message
from time import sleep

class SimTest:
    def __init__(self, showOutput = False):
        self.radio = Radio()
        self.fpi = FakePycomInterface()
        
        self.views = {}
        self.clients = {}
        self.showOutput = showOutput

    def callBack(nodeID, MessageBytes):
        print(MessageBytes)

    def add(self, nodeId, x, y):
        socket = SimulatorSocket(nodeId, x, y)
        self.radio.add(nodeId, socket)
        self.views[nodeId] = SimTestView(nodeId)
        
        self.clients[nodeId] = PymeshAdapter(self.views[nodeId], socket, self.fpi, SimTest.callBack)

    def disableRadio(self, nodeId):
        self.radio.disableRadio(nodeId)
    
    def clearMessages(self, nodeId):
        self.views[nodeId].clearMessages()


    def send(self, fromNodeID, to, message):
        self.clients[fromNodeID].sendMessage(to, message)

    def endSim(self):
        self.fpi.die()

    def processUntilSilent(self, secondsOfSilence):
        self.radio.processUntilSilent(secondsOfSilence)

    def assertHasMessage(self, nodeID, messageType):
        if messageType == Message.TYPE_ACC:
            t = "acc"
        elif messageType == Message.TYPE_FIND:
            t = "find"
        else:
            t = "message"
        hasMess = self.views[nodeID].hasMessage(messageType)
        assert hasMess, "No message on node " + str(nodeID) + " of type " + t
    
    def assertHasNoMessage(self, nodeID, messageType):
        if messageType == Message.TYPE_ACC:
            t = "acc"
        elif messageType == Message.TYPE_FIND:
            t = "find"
        else:
            t = "message"

        hasMess = self.views[nodeID].hasMessage(messageType)
        assert not hasMess, "No message on node " + str(nodeID) + " of type " + t
        
