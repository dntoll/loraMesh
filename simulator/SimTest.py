from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.SimView import SimView
from simulator.SimulatorSocket import SimulatorSocket
from mesh.PymeshAdapter import PymeshAdapter
from time import sleep

class SimTest:
    def __init__(self):
        self.radio = Radio()
        self.fpi = FakePycomInterface()
        
        self.clients = {}


    def add(self, nodeId, x, y):
        socket = SimulatorSocket(nodeId, x, y)
        self.radio.add(socket)
        sv = SimView(nodeId)
        self.clients[nodeId] = PymeshAdapter(sv, socket, self.fpi)

    def send(self, fromNodeID, to, message):
        self.clients[fromNodeID].sendMessage(to, message)

    def endSim(self):
        self.fpi.die()

    def wait(self, timesecs):
        timePerStep = 0.01

        for i in range(int( timesecs / timePerStep )):
            self.radio.process()
            sleep(timePerStep)

    def assertListen(self, node, messageType, messageContent):
        return
