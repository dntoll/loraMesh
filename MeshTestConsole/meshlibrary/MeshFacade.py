from meshlibrary.ThreadSafeLoraSocket import ThreadSafeLoraSocket
from meshlibrary.PycomInterface import PycomInterface
from meshlibrary.PymeshAdapter import PymeshAdapter

class MeshFacade:
    def __init__(self, view, callback):
        self.pma = PymeshAdapter(view, ThreadSafeLoraSocket(), PycomInterface())

    def getMyAddress(self):
        return self.pma.getMyAddress()

    def sendMessage(self, target_ip, message):
        self.pma.sendMessage(target_ip, message)

    def getKnownNodes(self):
        return self.pma.getKnownNodes()