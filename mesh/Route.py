

class Route:
    def __init__(self, bytes):
        self.route = bytes

    def getBytes(self):
        return self.route

    def getTarget(self):
        return self.route[len(self.route)-1]

    def getOrigin(self):
        return self.route[0]

    def getNumberOfJumps(self):
        return len(self.route)-1

    def getBackRoute(self):
        reversed = []
        for dest in self.route:
            reversed.insert(0, dest)

        return Route(bytes(reversed))
    
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

    #We can remove all not needed steps between sender and myMac
    def getSubRoute(self, senderOfMessage, myMac):

        ret = []
        foundSender = False
        foundMe = False
        for ref in self.route:
            if not foundSender:
                ret.append(ref) #include all up until and including sender
            if ref == senderOfMessage:
                foundSender = True
            if ref == myMac:
                foundMe = True
            if foundMe: #include me and all after
                ret.append(ref)

        return Route(bytes(ret))

    