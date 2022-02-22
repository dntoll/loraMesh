from mesh.ThreadSafeLoraSocket import ThreadSafeLoraSocket
from mesh.PycomInterface import PycomInterface
from mesh.PymeshAdapter import PymeshAdapter

class MeshFacade:
    def __init__(self, view, callback):
        self.pma = PymeshAdapter(view, ThreadSafeLoraSocket(), PycomInterface())

    def getMyAddress(self):
        return self.pma.getMyAddress()

    def sendMessage(self, target_ip, message):
        self.pma.sendMessage(target_ip, message)