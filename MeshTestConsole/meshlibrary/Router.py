# coding=utf-8



from meshlibrary.Route import Route
from meshlibrary.Neighbor import Neighbor



class Router:

    def __init__(self, pycomInterface, myMac):
        self.neighbors = {}
        self.routes = {}
        self.myMac = myMac
        self.pycomInterface = pycomInterface

    def deriveRouterData(self, message, receivedLoraStats):

        #receivedLoraStats from lora.stats() https://docs.pycom.io/firmwareapi/pycom/network/lora/
        
        if self.macIsNeighbour(message.senderMac): #update knowledge
            self.neighbors[message.senderMac].rssi = receivedLoraStats.rssi
            self.neighbors[message.senderMac].time = self.pycomInterface.ticks_ms()
        else:
            self.neighbors[message.senderMac] = Neighbor(message.senderMac, receivedLoraStats.rssi, self.pycomInterface.ticks_ms())
        
        verifiedRoute = message.route.getUpUntil(message.senderMac) #kan vi veta att sändaren finns med?

        
        self.neighbors[message.senderMac].addNodesBeyond(verifiedRoute)
        
        #Vi kan bara ha koll på den delen som går fram till oss eller sändaren, dvs verifierade router
        if message.route.notInRoute(self.myMac):
            
            verifiedRoute.addToEnd(self.myMac) #eftersom vi tagit emot detta så kan vi lägga till oss på slutet.
            self.routes[str(verifiedRoute.getBytes())] = verifiedRoute
        else:
            verifiedRoute = message.route.getUpUntil(self.myMac)
            self.routes[str(verifiedRoute.getBytes())] = verifiedRoute

        #this might not be valid since some might send more strongly than others
        #backRoute = message.route.getBackRoute()
        #self.routes[str(backRoute.getBytes())] =backRoute
        
    
    def getRoutes(self):
        return self.routes

    def getKnownNodes(self):
        ret = {}
        for n in self.neighbors:
            ret[self.neighbors[n].mac] = self.neighbors[n].mac

        for route in self.routes:
            parts = self.routes[route].getBytes()
            for n in parts:
                ret[n] = n

        return ret

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