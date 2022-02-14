

from mesh.Route import Route


class Neighbor:
    def __init__(self, mac, rssi, time):
        self.mac = mac
        self.rssi = rssi
        self.time = time

class Router:

    def __init__(self, pycomInterface):
        self.neighbors = {}
        self.routes = {}
        self.pycomInterface = pycomInterface

    def deriveRouterData(self, message, receivedLoraStats):

        #receivedLoraStats from lora.stats() https://docs.pycom.io/firmwareapi/pycom/network/lora/
        
        if self.macIsNeighbour(message.senderMac): #update knowledge
            self.neighbors[message.senderMac].rssi = receivedLoraStats.rssi
            self.neighbors[message.senderMac].time = self.pycomInterface.ticks_ms()
        else:
            self.neighbors[message.senderMac] = Neighbor(message.senderMac, receivedLoraStats.rssi, self.pycomInterface.ticks_ms())
        

        self.routes[str(message.route.getBytes())] = message.route

        #this might not be valid since some might send more strongly than others
        backRoute = message.route.getBackRoute()
        self.routes[str(backRoute.getBytes())] =backRoute
        
    
    def getRoutes(self):
        return self.routes

    def getNeighbors(self):
        return self.neighbors

    def getRoute(self, fromMac, toMac):
        if self.macIsNeighbour(toMac):
            route = bytearray(2)
            route[0] = fromMac
            route[1] = toMac
            return Route(bytes(route))
        
        for route in self.routes:
            if self.routes[route].bothInRouteAndOrdered(fromMac, toMac):
                return self.routes[route].getSubRoute(fromMac, toMac)
        
        raise Exception("No route found")
        

    def hasRoute(self, fromMac, toMac):
        if self.macIsNeighbour(toMac):
            return True
        
        if self.iHaveSeenRoute(fromMac, toMac):
            return True
        
        return False
    
    def macIsNeighbour(self, mac):
        if mac in self.neighbors:
            return True
        return False
    
    def iHaveSeenRoute(self, fromMac, toMac):
        for route in self.routes:
            if self.routes[route].bothInRouteAndOrdered(fromMac, toMac):
                return True
        
        return False