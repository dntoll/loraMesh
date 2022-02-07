
import utime
from mesh.Route import Route


class Neighbor:
    def __init__(self, mac, rssi, time):
        self.mac = mac
        self.rssi = rssi
        self.time = time

class Router:

    def __init__(self):
        self.neighbors = {}
        self.routes = {}

    def deriveRouterData(self, message, receivedLoraStats):

        #receivedLoraStats from lora.stats() https://docs.pycom.io/firmwareapi/pycom/network/lora/
        
        if message.senderMac in self.neighbors:
            self.neighbors[message.senderMac].rssi = receivedLoraStats.rssi
            self.neighbors[message.senderMac].time = utime.ticks_ms()
        else:
            self.neighbors[message.senderMac] = Neighbor(message.senderMac, receivedLoraStats.rssi, utime.ticks_ms())
        

        self.routes[str(message.route.getBytes())] = message.route

        backRoute = message.route.getBackRoute()
        self.routes[str(backRoute.getBytes())] =backRoute
        
    
    def getRoutes(self):
        return self.routes

    def getNeighbors(self):
        return self.neighbors

    def getRoute(self, fromMac, toMac):
        route = bytearray(2)
        route[0] = fromMac
        route[1] = toMac
        return Route.fromBytes(route)