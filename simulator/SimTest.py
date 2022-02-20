from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.SimTestView import SimTestView
from simulator.SimView import SimView
from view.CompositeView import CompositeView

from simulator.SimulatorSocket import SimulatorSocket
from mesh.PymeshAdapter import PymeshAdapter
from time import sleep

class SimTest:
    def __init__(self, showOutput = False):
        self.radio = Radio()
        self.fpi = FakePycomInterface()
        
        self.views = {}
        self.clients = {}
        self.showOutput = showOutput


    def add(self, nodeId, x, y):
        socket = SimulatorSocket(nodeId, x, y)
        self.radio.add(socket)
        self.views[nodeId] = SimTestView(nodeId)
        
        self.clients[nodeId] = PymeshAdapter(self.views[nodeId], socket, self.fpi)

    def send(self, fromNodeID, to, message):
        self.clients[fromNodeID].sendMessage(to, message)

    def endSim(self):
        self.fpi.die()

    def wait(self, steps):
        timePerStep = 0.1

        for i in range(steps):
            self.radio.process()
            sleep(timePerStep)

    def assertHasMessage(self, nodeID, messageType):
        assert self.views[nodeID].hasMessage(messageType), "No message on node " + str(nodeID) + " of type " + str(messageType)
    
    def assertHasNoMessage(self, nodeID, messageType):
        assert not self.views[nodeID].hasMessage(messageType), "No message on node " + str(nodeID) + " of type " + str(messageType)
        
