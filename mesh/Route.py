

class Route:
    def __init__(self, bytes):
        self.route = bytes

    def getBytes(self):
        return self.route

    def fromBytes(bytes):
        return Route(bytes)

    def getTarget(self):
        return self.route[len(self.route)-1]

    def getOrigin(self):
        return self.route[0]

    def getNumberOfJumps(self):
        return len(self.route)-1

    
    def IShouldRoute(self, senderOfMessage, potentialRouterMac):
        foundSender = False
        for ref in self.route:
            if ref == senderOfMessage:
                foundSender = True
            if ref == potentialRouterMac:
                if foundSender: #sender was part of route and is before us in send que => we route
                    return True

        #we are not in route or sender was after us...
        return False

    