

from mesh.Route import Route

class Router:

    def __init__(self):
        self.neighbors = []

    def deriveRouterData(self, message, receivedLoraStats):

        #receivedLoraStats from lora.stats() https://docs.pycom.io/firmwareapi/pycom/network/lora/
        self.neighbors.append(message.senderMac)
        self.neighbors.append(message.route)

    def getKnownRoutes(self):
        return self.neighbors

    def getRoute(self, fromMac, toMac):
        route = bytearray(2)
        route[0] = fromMac
        route[1] = toMac
        return Route.fromBytes(route)